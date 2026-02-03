import socketio
from app.agents.monitoring import session_monitor
from app.agents.risk import risk_detector
from app.agents.decision import decision_agent
from app.agents.executioner import executioner

sio_server = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins="*"
)

sio_app = socketio.ASGIApp(
    socketio_server=sio_server,
    socketio_path='socket.io'
)

# In-memory store for active connections (User -> SIDs)
# Still useful for fast lookups even with Redis
active_connections = {}

@sio_server.event
async def connect(sid, environ):
    # print(f"Client connected: {sid}")
    pass

@sio_server.event
async def join(sid, data):
    user_id = data.get('user_id')
    app_name = data.get('app_name', 'Unknown App')
    
    # Mock Metadata
    meta = {
        "ip": "127.0.0.1", # Mock
        "device": "Browser",
        "country": "US", # Default benign
        "app_name": app_name
    }
    
    if user_id:
        print(f"Client {sid} ({app_name}) joining room user_{user_id}")
        await sio_server.enter_room(sid, f"user_{user_id}")
        
        # Admin Room Join
        if "Admin" in app_name:
            print(f"🛡️ Client {sid} joined ADMIN ROOM")
            await sio_server.enter_room(sid, "admin_room")
        
        # 1. Register Session (Agent 1)
        session_monitor.register_session(user_id, sid, meta)
        
        # 2. Calculate Risk (Agent 2)
        score, reasons = risk_detector.calculate_risk(user_id, sid, meta)
        
        # NOTE: Real-time broadcast to Admin Dashboard
        await sio_server.emit('RISK_UPDATE', {
            'user_id': user_id,
            'app_name': app_name,
            'score': score,
            'reasons': reasons,
            'status': 'ACTIVE'
        }, room='admin_room')
        
        # 3. Auto-Decision (Agent 3)
        action = decision_agent.evaluate_risk(user_id, sid, score)
        
        print(f"🧠 [Brain] Risk: {score} | Action: {action} | Reasons: {reasons}")
        
        # 4. Execution (Agent 4)
        if action == "FORCE_LOGOUT" or action == "LOCK_ACCOUNT":
            await executioner.execute_global_logout(sio_server, user_id, f"High Risk ({score}): {', '.join(reasons)}")
            # Notify Admin of Action
            await sio_server.emit('RISK_UPDATE', {
                'user_id': user_id, 'app_name': app_name, 'score': score, 'status': 'KILLED'
            }, room='admin_room')
            
        elif action == "REQUIRE_REAUTH":
            await executioner.trigger_reauth(sio_server, user_id, sid)
            await sio_server.emit('RISK_UPDATE', {
                'user_id': user_id, 'app_name': app_name, 'score': score, 'status': 'CHALLENGED'
            }, room='admin_room')

@sio_server.event
async def heartbeat(sid, data):
    user_id = data.get('user_id')
    if user_id:
        session_monitor.heartbeat(user_id, sid)

@sio_server.event
async def verify_password(sid, data):
    """
    Called when user submits password in Re-Auth modal.
    """
    user_id = data.get('user_id')
    password = data.get('password')
    
    # Mock Verification (In real app, verify hash)
    if password == "password":
        executioner.log_success_reauth(user_id)
        # Notify client to close modal
        await sio_server.emit('REAUTH_SUCCESS', {'message': 'Verified'}, room=sid)
    else:
        await sio_server.emit('REAUTH_FAILED', {'message': 'Invalid Password'}, room=sid)

@sio_server.event
async def force_global_logout(sid, data):
    """
    Triggered by a client to force logout on all apps.
    """
    user_id = data.get('user_id')
    reason = data.get('reason', 'Manual Global Logout')
    initiator = data.get('initiator', 'Unknown')
    
    # Delegate to Executioner but we need to pass initiator info if we want to log it
    # For now, simplistic reuse
    await executioner.execute_global_logout(sio_server, user_id, f"{reason} (via {initiator})")

@sio_server.event
async def disconnect(sid):
    # print(f"Client disconnected: {sid}")
    pass
