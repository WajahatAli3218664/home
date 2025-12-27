"""
Monitoring for responses that might contain external knowledge
"""
from typing import Dict, List, Optional
from datetime import datetime
import json
import os


class MonitoringService:
    """
    Service for monitoring responses to detect potential external knowledge usage
    """
    
    def __init__(self):
        # In a real implementation, this would connect to a monitoring system
        # For now, we'll just log to a file
        self.log_file = os.getenv("MONITORING_LOG_FILE", "rag_monitoring.log")
        self.suspicious_responses = []
    
    def log_response(self, query: str, context: str, response: str, session_id: str, confidence_level: str):
        """
        Log a response for monitoring purposes
        """
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "session_id": session_id,
            "query": query,
            "context": context[:200] + "..." if len(context) > 200 else context,  # Truncate long context
            "response": response,
            "confidence_level": confidence_level,
            "flags": []
        }
        
        # Check for potential issues
        if self._has_external_knowledge_indicators(response):
            log_entry["flags"].append("external_knowledge_indicators")
        
        if self._has_unusually_high_confidence_for_poor_context(query, context, response, confidence_level):
            log_entry["flags"].append("high_confidence_low_relevance")
        
        # Write to log file
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
        
        # Store suspicious responses if flagged
        if log_entry["flags"]:
            self.suspicious_responses.append(log_entry)
    
    def _has_external_knowledge_indicators(self, response: str) -> bool:
        """
        Check if response contains indicators of external knowledge
        """
        external_indicators = [
            "current year",
            "today",
            "recently",
            "just announced",
            "the future",
            "latest",
            "most recent",
            "breaking news",
            "stock price",
            "weather",
            "live"
        ]
        
        response_lower = response.lower()
        for indicator in external_indicators:
            if indicator in response_lower:
                return True
        
        return False
    
    def _has_unusually_high_confidence_for_poor_context(self, query: str, context: str, response: str, confidence_level: str) -> bool:
        """
        Check if the confidence level seems inappropriate for the context-response match
        """
        # If the confidence is high but the context is very short, it might be suspicious
        if confidence_level.upper() == "HIGH" and len(context.strip()) < 50:
            # If the response is much longer than the context, it might be hallucinated
            if len(response) > len(context) * 3:
                return True
        
        return False
    
    def get_suspicious_responses(self) -> List[Dict]:
        """
        Get all responses that were flagged as potentially problematic
        """
        return self.suspicious_responses
    
    def generate_monitoring_report(self) -> Dict:
        """
        Generate a monitoring report with statistics
        """
        total_responses = self._count_total_logged_responses()
        flagged_responses = len(self.suspicious_responses)
        
        report = {
            "report_timestamp": datetime.utcnow().isoformat(),
            "total_responses_monitored": total_responses,
            "flagged_responses": flagged_responses,
            "flagging_rate": flagged_responses / total_responses if total_responses > 0 else 0,
            "common_flags": self._get_common_flags(),
            "recent_suspicious_responses": self.suspicious_responses[-5:]  # Last 5 suspicious responses
        }
        
        return report
    
    def _count_total_logged_responses(self) -> int:
        """
        Count the total number of logged responses (from the log file)
        """
        try:
            with open(self.log_file, "r", encoding="utf-8") as f:
                return len(f.readlines())
        except FileNotFoundError:
            return 0
    
    def _get_common_flags(self) -> Dict[str, int]:
        """
        Get statistics on the most common flags
        """
        flag_counts = {}
        for entry in self.suspicious_responses:
            for flag in entry.get("flags", []):
                flag_counts[flag] = flag_counts.get(flag, 0) + 1
        
        return flag_counts