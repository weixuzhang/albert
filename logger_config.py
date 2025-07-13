"""
Logging configuration for AI Agent Sandbox
Provides centralized logging setup with different levels and formatters.
"""

import logging
import os
from datetime import datetime
from typing import Optional


class LoggerConfig:
    """Centralized logging configuration for the AI Agent Sandbox"""
    
    @staticmethod
    def setup_logging(
        log_level: str = "INFO",
        log_file: Optional[str] = None,
        enable_console: bool = True
    ) -> None:
        """
        Setup logging configuration for the entire application
        
        Args:
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Optional log file path
            enable_console: Whether to enable console logging
        """
        
        # Create logs directory if it doesn't exist
        if log_file and not os.path.exists(os.path.dirname(log_file)):
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        # Clear existing handlers
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # Set log level
        numeric_level = getattr(logging, log_level.upper(), logging.INFO)
        root_logger.setLevel(numeric_level)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console handler
        if enable_console:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(numeric_level)
            console_handler.setFormatter(formatter)
            root_logger.addHandler(console_handler)
        
        # File handler
        if log_file:
            file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
            file_handler.setLevel(numeric_level)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
        
        # Log startup message
        logging.info(f"AI Agent Sandbox logging initialized - Level: {log_level}")
    
    @staticmethod
    def get_default_log_file() -> str:
        """Get default log file path"""
        timestamp = datetime.now().strftime("%Y%m%d")
        return f"logs/ai_agent_sandbox_{timestamp}.log"
    
    @staticmethod
    def log_agent_activity(agent_name: str, activity: str, details: Optional[str] = None) -> None:
        """
        Log agent activity with structured format
        
        Args:
            agent_name: Name of the agent
            activity: Description of the activity
            details: Optional additional details
        """
        logger = logging.getLogger(f"agent.{agent_name.lower().replace(' ', '_')}")
        message = f"[{agent_name}] {activity}"
        if details:
            message += f" - {details}"
        logger.info(message)
    
    @staticmethod
    def log_api_call(api_name: str, status: str, response_time: Optional[float] = None, 
                    error: Optional[str] = None) -> None:
        """
        Log API calls with structured format
        
        Args:
            api_name: Name of the API
            status: Status of the call (success, error, retry, etc.)
            response_time: Response time in seconds
            error: Error message if any
        """
        logger = logging.getLogger("api")
        message = f"[{api_name}] {status}"
        
        if response_time is not None:
            message += f" - {response_time:.2f}s"
        
        if error:
            message += f" - Error: {error}"
            logger.error(message)
        elif status.lower() == 'success':
            logger.info(message)
        else:
            logger.warning(message)
    
    @staticmethod
    def log_user_interaction(user_input: str, processing_time: Optional[float] = None, 
                           success: bool = True) -> None:
        """
        Log user interactions for monitoring and analytics
        
        Args:
            user_input: User's input (truncated for privacy)
            processing_time: Time taken to process the request
            success: Whether the processing was successful
        """
        logger = logging.getLogger("user_interaction")
        
        # Truncate user input for privacy and log size
        truncated_input = user_input[:100] + "..." if len(user_input) > 100 else user_input
        
        message = f"User request processed: '{truncated_input}'"
        
        if processing_time is not None:
            message += f" - Processing time: {processing_time:.2f}s"
        
        message += f" - Status: {'SUCCESS' if success else 'FAILED'}"
        
        if success:
            logger.info(message)
        else:
            logger.warning(message)


# Initialize default logging when module is imported
def initialize_default_logging():
    """Initialize default logging configuration"""
    log_level = os.getenv('AI_SANDBOX_LOG_LEVEL', 'INFO')
    enable_file_logging = os.getenv('AI_SANDBOX_FILE_LOGGING', 'true').lower() == 'true'
    
    log_file = None
    if enable_file_logging:
        log_file = LoggerConfig.get_default_log_file()
    
    LoggerConfig.setup_logging(
        log_level=log_level,
        log_file=log_file,
        enable_console=True
    )


# Initialize on import
initialize_default_logging()