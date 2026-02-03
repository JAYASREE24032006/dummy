from app.core.redis_client import redis_client
import time

class AutoDecisionAgent:
    def __init__(self):
        self.redis = redis_client

    def evaluate_risk(self, user_id, session_id, current_score):
        """
        Evaluates risk score and determines action.
        Returns: Action String (SAFE, WARNING, REQUIRE_REAUTH, FORCE_LOGOUT, LOCK_ACCOUNT)
        """
        # Get Last Reauth Timestamp
        last_reauth_key = f"user:{user_id}:last_reauth"
        last_reauth_ts = self.redis.get_client().get(last_reauth_key)
        
        is_in_grace_period = False
        if last_reauth_ts:
            diff = time.time() - float(last_reauth_ts)
            if diff < 900: # 15 minutes
                is_in_grace_period = True
        
        action = "SAFE"
        
        if current_score > 95:
            return "LOCK_ACCOUNT"
        
        if current_score > 85:
            # Critical Level - IGNORE Grace Period
            return "FORCE_LOGOUT"
            
        if current_score > 65:
            # Soft Level - Check Grace Period
            if is_in_grace_period:
                print(f"⚖️ [Judge] Grace Period Active. Downgrading REAUTH to WARNING.")
                return "WARNING"
            else:
                return "REQUIRE_REAUTH"
                
        if current_score > 50:
            return "WARNING"
            
        return "SAFE"

decision_agent = AutoDecisionAgent()
