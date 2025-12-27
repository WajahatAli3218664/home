import logging
import sys
from datetime import datetime
from typing import Dict, Any, Optional
from ..models.debug_log import DebugLog


def setup_logging():
    """Set up logging configuration for context flow tracking"""
    # Configure the root logger
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("logs/debug_rag.log", mode="a")
        ]
    )
    
    # Create a logger for RAG context tracking
    rag_logger = logging.getLogger("rag_context")
    rag_logger.setLevel(logging.DEBUG)
    
    return rag_logger


def log_context_flow(
    component: str,
    message: str,
    context_data: Optional[Dict[str, Any]] = None,
    level: str = "info"
) -> DebugLog:
    """
    Create a debug log entry for context flow tracking
    """
    log_entry = DebugLog(
        id=f"debug_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
        timestamp=datetime.now(),
        component=component,
        message=message,
        context_snapshot=context_data,
        level=level
    )
    
    # Also log to the standard logger
    rag_logger = setup_logging()
    getattr(rag_logger, level)(f"[{component}] {message}")
    
    return log_entry