from fastapi import APIRouter, Depends, HTTPException, status, Header, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.auth.jwt import create_access_token, create_refresh_token
from app.core.database import get_redis
from app.auth.websockets import sio_server
from pydantic import BaseModel
import json

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(), 
    redis=Depends(get_redis)
):
    # Determine Client IP
    # In a real app behind a proxy, use X-Forwarded-For
    # For this demo, we AUTO-DETECT based on the "Source" (simulated by username)
    client_ip = request.client.host
    
    # 🕵️‍♂️ AUTOMATIC DETECTION SIMULATION
    # If the attacker tries to login, we simulate that they are coming from a known VPN IP.
    if form_data.username == "attacker" or form_data.username == "vpn_user":
        client_ip = "185.200.118.45" # Example known VPN IP
    elif form_data.username == "user":
        client_ip = "127.0.0.1"
    else:
        # Default fallback
        client_ip = request.client.host
    # Mock user verification
    valid_usernames = ["admin", "attacker", "user"]
    if form_data.username not in valid_usernames or form_data.password != "password":
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    user_id = "user_123" # Mock User ID
    
    # Create tokens
    access_token = create_access_token(data={"sub": user_id})
    refresh_token = create_refresh_token(data={"sub": user_id})
    
    # Is this a new device? (Simulated for now)
    # Store session in Redis
    # decode to get JTI
    from jose import jwt
    from app.core.config import settings
    
    decoded_at = jwt.decode(access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    jti = decoded_at['jti']
    
    # Store JTI in user's session list
    await redis.sadd(f"user:{user_id}:sessions", jti)
    
    # Store Refresh Token
    await redis.setex(f"refresh_token:{jti}", settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400, refresh_token)

    # --- AGENTIC LAYER HOOK ---
    # Integration with new Agentic System
    from app.agents.risk import risk_detector
    from app.agents.decision import decision_agent
    
    # Create Meta for Risk Agent
    
    # 🕵️‍♂️ MOCK GEO-LOCATION
    detected_country = "India"
    if form_data.username == "attacker":
        detected_country = "Russia" # Simulate Foreign Attack
        
    meta = {
        "ip": client_ip,
        "device": "Browser (Login)", 
        "country": detected_country, 
        "app_name": "Login Portal" 
    }
    
    # 1. Calculate Risk
    # This uses the Sync Redis Client internally, which is fine for prototype limits
    current_score, reasons = risk_detector.calculate_risk(user_id, jti, meta)
    
    print(f"🤖 Agentic Analysis: Login Attempt from {client_ip} | Risk: {current_score}")

    # 2. Make Decision
    action = decision_agent.evaluate_risk(user_id, jti, current_score)
    
    if action == "FORCE_LOGOUT" or action == "LOCK_ACCOUNT":
        print(f"❌ RISK DETECTED ({current_score}). TRIGGERING GLOBAL LOCKDOWN.")
        await global_revoke(user_id, redis)
        raise HTTPException(
            status_code=403, 
            detail=f"Security Alert: High Risk Detected ({current_score}). Access Denied."
        )
    # --------------------------


    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "refresh_token": refresh_token,
        "jti": jti
    }

@router.post("/revoke")
async def revoke(token: str = Depends(oauth2_scheme), redis=Depends(get_redis)):
    # Revoke simple access token (logout current session)
    from jose import jwt
    from app.core.config import settings
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        jti = payload.get("jti")
        user_id = payload.get("sub")
        
        if jti:
            await redis.setex(f"blacklist:{jti}", settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60, "true")
            await redis.srem(f"user:{user_id}:sessions", jti)
            await redis.delete(f"refresh_token:{jti}")
            
    except Exception:
        pass
        
    return {"msg": "Token revoked"}

@router.post("/global-revoke")
async def global_revoke(user_id: str = "user_123", redis=Depends(get_redis)): # In real app, get user_id from token
    # 1. Iterate through all active sessions
    sessions = await redis.smembers(f"user:{user_id}:sessions")
    
    for jti in sessions:
        # Blacklist JTI
        await redis.setex(f"blacklist:{jti}", 3600, "true") # Blacklist for 1 hr
        # Delete Refresh Token
        await redis.delete(f"refresh_token:{jti}")
    
    # Clear session list
    await redis.delete(f"user:{user_id}:sessions")
    
    # Emit LOGOUT_ALL signal to the user's room
    await sio_server.emit('LOGOUT_ALL', {'user_id': user_id}, room=f"user_{user_id}")
    
    return {"msg": "All sessions revoked"}

@router.post("/refresh")
async def refresh_token(refresh_token: str, redis=Depends(get_redis)):
    from jose import jwt, JWTError
    from app.core.config import settings
    
    try:
        # 1. Decode & Validate
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        old_jti = payload.get("jti")
        
        if not user_id or not old_jti:
            raise HTTPException(status_code=401, detail="Invalid token")
            
        # 2. Check if blacklisted/revoked
        is_revoked = await redis.get(f"blacklist:{old_jti}")
        if is_revoked:
             # Security Event: Token Reuse Detected!
             # Trigger Risk Agent? For now, just hard fail.
             raise HTTPException(status_code=401, detail="Token revoked")
             
        # 3. Rotate Token
        # Revoke the old one
        await redis.setex(f"blacklist:{old_jti}", settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400, "rotated")
        await redis.delete(f"refresh_token:{old_jti}")
        await redis.srem(f"user:{user_id}:sessions", old_jti)
        
        # Issue New Tokens
        import uuid
        new_jti = str(uuid.uuid4())
        
        access_token_data = {"sub": user_id, "jti": new_jti}
        refresh_token_data = {"sub": user_id, "jti": new_jti}
        
        from app.auth.jwt import create_access_token, create_refresh_token
        new_access_token = create_access_token(access_token_data)
        new_refresh_token = create_refresh_token(refresh_token_data)
        
        # 4. Register New Session
        await redis.sadd(f"user:{user_id}:sessions", new_jti)
        await redis.setex(f"refresh_token:{new_jti}", settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400, new_refresh_token)
        
        # 5. Update Monitoring (Link new session to old metadata or create new?)
        # Ideally, we copy metadata from old session to new, to keep track of "Device".
        # For prototype, we can just let it be. Or capture signal again if we had headers.
        
        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
            "jti": new_jti
        }
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
