import socketio
from app.agents.monitoring import session_monitor
from app.agents.risk import risk_detector
from app.agents.decision import decision_agent
from app.agents.executioner import executioner

# Using In-Memory Manager for Local Prototype Reliability
sio_server = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins="*"
)

sio_app = socketio.ASGIApp(
    socketio_server=sio_server,
    socketio_path='socket.io'
)

# Explicit In-Memory Session Store
# Maps user_id -> set({sid1, sid2, ...})
active_user_sessions = {}

@sio_server.event
async def connect(sid, environ):
    # print(f"Client connected: {sid}")
    pass

@sio_server.event
async def join(sid, data):
    user_id = data.get('user_id')
    app_name = data.get('app_name', 'Unknown App')
    
    if user_id:
        print(f"✅ [Socket] Client {sid} ({app_name}) joined user_{user_id}")
        await sio_server.enter_room(sid, f"user_{user_id}")
        
        # Manual Tracking
        if user_id not in active_user_sessions:
            active_user_sessions[user_id] = set()
        active_user_sessions[user_id].add(sid)
        
        # Risk Analysis
        # Mocking Location: In real app, derived from IP via GeoIP DB
        meta = {"ip": "127.0.0.1", "app_name": app_name, "country": "India"}
        await session_monitor.register_session(user_id, sid, meta)
        
        # Trigger Risk Check
        score, reasons = await risk_detector.calculate_risk(user_id, sid, meta)
        
        # Auto-Execution Logic
        action = await decision_agent.evaluate_risk(user_id, sid, score)
        if action == "FORCE_LOGOUT":
             await executioner.execute_global_logout(sio_server, user_id, f"High Risk: {reasons}")

@sio_server.event
async def disconnect(sid):
    # Remove SID from all trackers
    for uid in list(active_user_sessions.keys()):
        if sid in active_user_sessions[uid]:
            active_user_sessions[uid].remove(sid)
            if not active_user_sessions[uid]:
                del active_user_sessions[uid]
            break

@sio_server.event
async def force_global_logout(sid, data):
    user_id = data.get('user_id')
    reason = data.get('reason', 'Manual Global Logout')
    initiator = data.get('initiator', 'Unknown')
    
    print(f"🌍 [Socket] Global Logout Initiated for {user_id} by {initiator}")
    
    # robust broadcast
    if user_id in active_user_sessions:
        target_sids = list(active_user_sessions[user_id])
        print(f"Messaging {len(target_sids)} active sessions...")
        for target_sid in target_sids:
            try:
                await sio_server.emit('LOGOUT_ALL', {
                    'user_id': str(user_id), # Ensure string for comparison
                    'reason': reason,
                    'initiator': initiator
                }, room=target_sid) # Direct messaging
            except Exception as e:
                print(f"Error sending to {target_sid}: {e}")
                
    # Also emit to room as backup
    await sio_server.emit('LOGOUT_ALL', {
        'user_id': str(user_id),
        'reason': reason,
        'initiator': initiator
    }, room=f"user_{user_id}")

@sio_server.event
async def heartbeat(sid, data):
    pass

@sio_server.event
async def verify_password(sid, data):
    user_id = data.get('user_id')
    password = data.get('password')
    if password == "password":
        await sio_server.emit('REAUTH_SUCCESS', {'message': 'Verified'}, room=sid)
    else:
        await sio_server.emit('REAUTH_FAILED', {'message': 'Invalid Password'}, room=sid)

