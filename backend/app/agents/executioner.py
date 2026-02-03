from app.core.redis_client import redis_client
import time

# We need access to the send_message capability. 
# Since this agent is called from websockets.py (where sio_server exists), 
# we might pass the server or a callback, OR we define the logic here and 
# websockets.py calls it and handles the emission.
# Better design: Executioner RETURNS the instruction payload, and the caller (Controller) emits it.
# OR Executioner acts on Data.
# Let's make Executioner hold the logic for WHAT to do.

class ForcedLogoutAgent:
    def __init__(self):
        self.redis = redis_client

    async def execute_global_logout(self, sio_server, user_id, reason):
        """
        Kills all active sessions for a user.
        """
        print(f"🛑 [Executioner] Executing GLOBAL LOGOUT for {user_id}. Reason: {reason}")
        
        # 1. Blacklist tokens (Mock or Redis Set)
        # self.redis.sadd(f"blacklist:{user_id}", current_token)
        
        # 2. Emit Signal
        await sio_server.emit('LOGOUT_ALL', {
            'user_id': user_id, 
            'reason': reason,
            'initiator': 'Security AI Agent'
        }, room=f"user_{user_id}")
        
        # 3. Disconnect Sockets (handled via room broadcast usually, but force disconnect logic is in websockets loop)
        # Ideally, we find all active SIDs and disconnect them provided we have access.
        # We will assume the frontend handles the LOGOUT_ALL by disconnecting itself, 
        # but server-side disconnect is safer. 
        # We can implement that in the caller or pass the list logic here.
        pass # Actual disconnect loop can be in the controller

    async def trigger_reauth(self, sio_server, user_id, session_id):
        """
        Sends a Re-Auth signal to a specific session (or all).
        Usually Re-Auth is session specific if caused by rapid switching on THAT device.
        """
        print(f"🛡️ [Executioner] Triggering RE-AUTH for {user_id} (Session: {session_id})")
        # We need the SID for this session_id. 
        # If we stored SID in Redis, we could fetch it.
        # For now, we will emit to the USER ROOM, but with a specific session_id in payload?
        # Or just require re-auth for everyone? Let's target the user room for simplicity of prototype.
        await sio_server.emit('REQUIRE_REAUTH', {
            'user_id': user_id,
            'reason': 'Risk Threshold Exceeded'
        }, room=f"user_{user_id}")

    def log_success_reauth(self, user_id):
        key = f"user:{user_id}:last_reauth"
        self.redis.get_client().set(key, str(time.time()))
        print(f"✅ [Executioner] Re-Auth Verified. Grace Period Started.")

executioner = ForcedLogoutAgent()
