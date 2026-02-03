from app.core.redis_client import redis_client
from app.agents.decision import decision_agent

class TokenLifecycleAgent:
    def __init__(self):
        self.redis = redis_client
        self.decision = decision_agent

    def validate_refresh(self, user_id, current_score):
        """
        Validates if a refresh token should be honored based on risk.
        Returns: (allow: bool, action: str)
        """
        # We assume the caller (API layer) has fetched the current score 
        # or we fetch it here. We'll pass it in for efficiency.
        
        # Determine action
        # Note: We technically don't have a session_id here during refresh easily unless 
        # the token contains it. We'll assume User-Level decision for now.
        action = self.decision.evaluate_risk(user_id, "refresh_flow", current_score)
        
        if action == "SAFE" or action == "WARNING":
            return True, "RefreshToken Granted"
        
        if action == "REQUIRE_REAUTH":
            print(f"🔄 [Token Agent] Refresh DENIED. Re-Auth Required for {user_id} (Score: {current_score})")
            return False, "High Risk: Re-Authentication Required"
            
        if action == "FORCE_LOGOUT" or action == "LOCK_ACCOUNT":
             print(f"🚫 [Token Agent] Refresh DENIED. Account Locked/Logged Out.")
             return False, "Security Alert: Session Terminated"
             
        return True, "Granted"

token_lifecycle = TokenLifecycleAgent()
