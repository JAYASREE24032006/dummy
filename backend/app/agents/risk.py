from app.core.redis_client import redis_client
from app.agents.monitoring import session_monitor
import time
from datetime import datetime

class RiskDetectionAgent:
    def __init__(self):
        self.redis = redis_client
        self.monitor = session_monitor

    def calculate_risk(self, user_id, session_id, current_meta):
        """
        Calculates the risk score for a session event.
        Returns: (total_score, reasons_list)
        """
        total_score = 0
        reasons = []

        # 1. Base Risks (New Device, Location)
        # In a real app, successful previous logins would be stored for comparison.
        # For prototype, we mock "New Country" if 'country' is not 'US'.
        country = current_meta.get('country', 'US')
        if country != 'US':
             total_score += 50
             reasons.append(f"New Country Detected: {country} (+50)")

        # 2. High Concurrency (>3 Sessions)
        active_sessions = self.monitor.get_active_sessions(user_id)
        if len(active_sessions) > 3:
            total_score += 30
            reasons.append(f"High Concurrency: {len(active_sessions)} Active Sessions (+30)")

        # 3. Abnormal Login Time (11 PM - 5 AM)
        current_hour = datetime.now().hour
        if current_hour >= 23 or current_hour < 5:
            total_score += 15
            reasons.append(f"Abnormal Login Time: {current_hour}:00 (+15)")

        # 4. Rapid App Switching (< 10 seconds)
        # Check last switch time stored in Redis User Profile or Session
        # For User-level switching, we need a user-level key
        last_switch_key = f"user:{user_id}:last_app_switch"
        last_switch_time = self.redis.get_client().get(last_switch_key)
        now = time.time()
        
        if last_switch_time:
            diff = now - float(last_switch_time)
            if diff < 10:
                total_score += 20
                reasons.append(f"Rapid App Switching: {int(diff)}s interval (+20)")
        
        # Update last switch time
        self.redis.get_client().set(last_switch_key, str(now))

        # Update Session Risk in Redis
        key = self.redis.session_key(user_id, session_id)
        # Get existing score to accumulate or overwrite? 
        # Usually risk is recalculated per event or accumulated. 
        # For simplicity, we overwrite total risk based on current state (stateful check)
        # OR we add behavior points to a base.
        # Let's overwrite "Current Session Risk" but behavior spikes (like rapid switch) 
        # might need to persist. 
        # Current Logic: Calculated from scratch based on current state.
        
        self.redis.hset(key, {"risk_score": str(total_score)})
        
        if total_score > 0:
            print(f"⚠️ [Risk Agent] Risk {total_score} for {user_id}: {', '.join(reasons)}")
            
        return total_score, reasons

    def update_risk_score(self, user_id, session_id, score):
        key = self.redis.session_key(user_id, session_id)
        self.redis.hincrby(key, "risk_score", score)

risk_detector = RiskDetectionAgent()
