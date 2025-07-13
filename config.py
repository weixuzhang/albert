"""
Configuration module for AI Agent Sandbox Prototype
Handles OpenAI API settings and system configurations.
"""

import os
import logging
from typing import Optional


class Config:
    """Configuration class for the AI Agent Sandbox system"""
    
    # OpenAI API Configuration
    OPENAI_API_KEY: Optional[str] = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL: str = "gpt-4o"  # GPT-4 Omni model
    OPENAI_MAX_TOKENS: int = 2000
    OPENAI_TEMPERATURE: float = 0.7
    
    # Agent Configuration
    ENABLE_AI_AGENTS: bool = True  # Set to False to use simple rule-based agents
    FALLBACK_TO_SIMPLE_AGENTS: bool = True  # Fallback if OpenAI API fails
    
    # System Configuration
    MAX_RETRIES: int = 3
    TIMEOUT_SECONDS: int = 30
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv('AI_SANDBOX_LOG_LEVEL', 'INFO')
    ENABLE_FILE_LOGGING: bool = os.getenv('AI_SANDBOX_FILE_LOGGING', 'true').lower() == 'true'
    
    # Security Configuration
    MAX_INPUT_LENGTH: int = 10000
    MAX_RESPONSE_LENGTH: int = 5000
    
    @classmethod
    def validate_openai_config(cls) -> bool:
        """
        Validate OpenAI configuration
        
        Returns:
            bool: True if configuration is valid
        """
        if not cls.OPENAI_API_KEY:
            print("[WARNING] OPENAI_API_KEY not found in environment variables")
            print("[INFO] Please set your OpenAI API key:")
            print("[INFO] export OPENAI_API_KEY='your-api-key-here'")
            return False
        
        if not cls.OPENAI_MODEL:
            print("[WARNING] OPENAI_MODEL not specified")
            return False
            
        return True
    
    @classmethod
    def get_openai_config(cls) -> dict:
        """
        Get OpenAI configuration as dictionary
        
        Returns:
            dict: OpenAI configuration parameters
        """
        return {
            'model': cls.OPENAI_MODEL,
            'max_tokens': cls.OPENAI_MAX_TOKENS,
            'temperature': cls.OPENAI_TEMPERATURE,
            'timeout': cls.TIMEOUT_SECONDS
        }
    
    @classmethod
    def display_config(cls) -> None:
        """Display current configuration"""
        print("AI Agent Sandbox Configuration")
        print("=" * 40)
        print(f"OpenAI API Key: {'Set' if cls.OPENAI_API_KEY else 'Not Set'}")
        print(f"OpenAI Model: {cls.OPENAI_MODEL}")
        print(f"Max Tokens: {cls.OPENAI_MAX_TOKENS}")
        print(f"Temperature: {cls.OPENAI_TEMPERATURE}")
        print(f"AI Agents Enabled: {'Enabled' if cls.ENABLE_AI_AGENTS else 'Disabled'}")
        print(f"Fallback to Simple Agents: {'Enabled' if cls.FALLBACK_TO_SIMPLE_AGENTS else 'Disabled'}")
        print(f"Max Retries: {cls.MAX_RETRIES}")
        print(f"Timeout: {cls.TIMEOUT_SECONDS}s")
        print(f"Log Level: {cls.LOG_LEVEL}")
        print(f"File Logging: {'Enabled' if cls.ENABLE_FILE_LOGGING else 'Disabled'}")
        
        logging.info("Configuration displayed to user")


# Agent-specific prompts and instructions
class AgentPrompts:
    """Prompts and instructions for each AI agent"""
    
    ALBERT_CORE_SYSTEM_PROMPT = """
You are Albert Core, the main user-facing interface of an AI Agent Sandbox system.

Your role:
- Receive and process initial user inputs
- Provide immediate, helpful responses
- Categorize requests for appropriate handling
- Act as the friendly, knowledgeable entry point

Guidelines:
- Be conversational and helpful
- Acknowledge the user's request clearly
- Explain what you'll coordinate with other agents
- Keep responses concise but informative
- Show understanding of the user's intent

Always maintain a professional yet approachable tone.
"""

    PLANNING_AGENT_SYSTEM_PROMPT = """
You are the Planning Agent in an AI Agent Sandbox system.

Your role:
- Analyze Albert Core's initial assessment
- Create structured, step-by-step plans
- Break down complex requests into manageable tasks
- Prioritize tasks appropriately
- Estimate time and resources needed

Guidelines:
- Create 3-6 well-defined tasks
- Use clear, actionable descriptions
- Assign appropriate priorities (high, medium, low)
- Consider different categories: planning, problem_solving, project, event, general
- Include realistic time estimates
- Think about dependencies between tasks

Focus on creating practical, executable plans that address the user's needs comprehensively.
"""

    QUESTIONING_AGENT_SYSTEM_PROMPT = """
You are the Questioning Agent (Slot Filler) in an AI Agent Sandbox system.

Your role:
- Review plans from the Planning Agent
- Identify missing or ambiguous details
- Generate clarifying questions
- Suggest improvements to make plans more complete
- Calculate completeness scores

Guidelines:
- Look for missing details: timelines, resources, stakeholders, success criteria
- Generate 3-8 relevant clarifying questions
- Focus on practical, actionable questions
- Identify gaps that would prevent successful execution
- Suggest specific improvements
- Be thorough but not overwhelming

Your goal is to ensure plans are complete, clear, and executable.
"""


class SecurityConfig:
    """Security configuration and validation rules"""
    
    # Input validation patterns
    SUSPICIOUS_PATTERNS = [
        r'<script[^>]*>.*?</script>',  # Script tags
        r'javascript:',  # JavaScript URLs
        r'data:.*base64',  # Data URLs
        r'eval\s*\(',  # eval() calls
        r'exec\s*\(',  # exec() calls
    ]
    
    # Rate limiting (future implementation)
    MAX_REQUESTS_PER_MINUTE = 60
    MAX_REQUESTS_PER_HOUR = 1000
    
    @classmethod
    def is_input_safe(cls, user_input: str) -> bool:
        """
        Check if user input is safe based on security patterns
        
        Args:
            user_input: User input to validate
            
        Returns:
            bool: True if input appears safe
        """
        import re
        
        for pattern in cls.SUSPICIOUS_PATTERNS:
            if re.search(pattern, user_input, re.IGNORECASE):
                logging.warning(f"Suspicious pattern detected: {pattern}")
                return False
        
        return True 