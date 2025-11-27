"""
Base Agent Class for ZenFeed Multi-Agent System

All agents inherit from this base class to ensure consistent interface
and communication patterns.
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime


class BaseAgent:
    """
    Base class for all ZenFeed agents.
    
    Provides:
    - Standard process() interface
    - Logging capabilities
    - Communication with orchestrator
    - Error handling framework
    """
    
    def __init__(self, name: str, orchestrator: Optional[Any] = None):
        """
        Initialize base agent.
        
        Args:
            name: Human-readable agent name
            orchestrator: Reference to orchestrator for inter-agent communication
        """
        self.name = name
        self.orchestrator = orchestrator
        self.logger = logging.getLogger(f"ZenFeed.{name}")
        self._setup_logging()
    
    def _setup_logging(self):
        """Configure logging for this agent."""
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            f'[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def log(self, message: str, level: str = "INFO"):
        """
        Log a message with the specified level.
        
        Args:
            message: Message to log
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        log_method = getattr(self.logger, level.lower(), self.logger.info)
        log_method(message)
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process input data and return results.
        
        This method must be implemented by all child agents.
        
        Args:
            data: Input data dictionary
            
        Returns:
            Dictionary containing processing results
            
        Raises:
            NotImplementedError: If child class doesn't implement this method
        """
        raise NotImplementedError(
            f"{self.name} must implement process() method"
        )
    
    def send_to_orchestrator(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Send a message to the orchestrator.
        
        Args:
            message: Message dictionary to send
            
        Returns:
            Response from orchestrator, if any
        """
        if self.orchestrator:
            return self.orchestrator.receive_message(self.name, message)
        else:
            self.log("No orchestrator connected", "WARNING")
            return None
    
    def validate_input(self, data: Dict[str, Any], required_fields: list) -> bool:
        """
        Validate that input data contains all required fields.
        
        Args:
            data: Input data to validate
            required_fields: List of required field names
            
        Returns:
            True if all required fields present, False otherwise
        """
        missing = [field for field in required_fields if field not in data]
        if missing:
            self.log(f"Missing required fields: {missing}", "ERROR")
            return False
        return True
    
    def create_response(
        self, 
        status: str, 
        data: Dict[str, Any], 
        error: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a standardized response dictionary.
        
        Args:
            status: Status string (success, error, partial)
            data: Response data
            error: Error message if status is error
            
        Returns:
            Standardized response dictionary
        """
        response = {
            "agent": self.name,
            "status": status,
            "timestamp": datetime.utcnow().isoformat(),
            "data": data
        }
        if error:
            response["error"] = error
        return response
    
    def handle_error(self, error: Exception, context: str = "") -> Dict[str, Any]:
        """
        Handle an error and return error response.
        
        Args:
            error: The exception that occurred
            context: Additional context about where error occurred
            
        Returns:
            Error response dictionary
        """
        error_msg = f"{context}: {str(error)}" if context else str(error)
        self.log(error_msg, "ERROR")
        return self.create_response(
            status="error",
            data={},
            error=error_msg
        )
