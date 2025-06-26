"""
Albert Core Agent - Main user-facing interface
Receives and processes initial user inputs, provides immediate responses or preliminary processing.
Enhanced with OpenAI GPT-4 capabilities.
"""

from typing import Dict, Any
from json_schemas import JSONSchemas
from config import Config, AgentPrompts
from openai_utils import get_ai_response


class AlbertCore:
    """
    Albert Core agent handles direct user interaction and provides initial processing.
    Acts as the entry point for all user requests in the AI Agent Sandbox.
    """
    
    def __init__(self):
        """Initialize Albert Core agent"""
        self.agent_name = "Albert Core"
        self.version = "1.0.0"
    
    def process_user_input(self, user_input: str) -> Dict[str, Any]:
        """
        Process user input and generate structured JSON response.
        
        Args:
            user_input (str): The user's input message
            
        Returns:
            Dict[str, Any]: Structured response following albert_core_schema
        """
        
        # Handle empty or invalid input
        if not user_input or not isinstance(user_input, str) or not user_input.strip():
            return JSONSchemas.albert_core_schema(
                user_input=user_input or "",
                response="",
                error="Invalid or empty input provided"
            )
        
        # Clean the input
        cleaned_input = user_input.strip()
        
        # Generate response based on input analysis
        response = self._generate_response(cleaned_input)
        
        # Return structured JSON output
        return JSONSchemas.albert_core_schema(
            user_input=cleaned_input,
            response=response
        )
    
    def _generate_response(self, user_input: str) -> str:
        """
        Generate appropriate response based on user input analysis.
        Uses OpenAI GPT-4 if available, falls back to simple rules otherwise.
        
        Args:
            user_input (str): Cleaned user input
            
        Returns:
            str: Generated response
        """
        
        # Try to use OpenAI API if enabled and configured
        if Config.ENABLE_AI_AGENTS:
            ai_response = self._get_ai_response(user_input)
            if ai_response:
                return ai_response
        
        # Fallback to simple rule-based response generation
        if Config.FALLBACK_TO_SIMPLE_AGENTS:
            return self._get_simple_response(user_input)
        
        return "I'm sorry, I'm unable to process your request at the moment. Please try again later."
    
    def _get_ai_response(self, user_input: str) -> str:
        """
        Get AI-powered response using OpenAI GPT-4
        
        Args:
            user_input (str): User input
            
        Returns:
            str: AI-generated response or empty string if failed
        """
        
        try:
            messages = [
                {
                    "role": "user", 
                    "content": f"User request: {user_input}\n\nPlease provide a helpful initial response and explain how you'll coordinate with other agents to help."
                }
            ]
            
            ai_response = get_ai_response(
                messages=messages,
                system_prompt=AgentPrompts.ALBERT_CORE_SYSTEM_PROMPT
            )
            
            if isinstance(ai_response, str):
                return ai_response.strip()
            elif isinstance(ai_response, dict) and 'response' in ai_response:
                return ai_response['response'].strip()
            
        except Exception as e:
            print(f"⚠️  Albert Core AI response failed: {e}")
        
        return ""
    
    def _get_simple_response(self, user_input: str) -> str:
        """
        Get simple rule-based response (fallback)
        
        Args:
            user_input (str): User input
            
        Returns:
            str: Simple rule-based response
        """
        
        input_lower = user_input.lower()
        
        # Planning-related requests
        if any(keyword in input_lower for keyword in ['plan', 'organize', 'schedule', 'prepare']):
            return f"I can help you create a plan for: {user_input}. Let me coordinate with the planning agent to develop a structured approach."
        
        # Question-related requests
        elif any(keyword in input_lower for keyword in ['question', 'ask', 'clarify', 'explain']):
            return f"I understand you need clarification about: {user_input}. I'll work with our questioning agent to provide detailed answers."
        
        # Problem-solving requests
        elif any(keyword in input_lower for keyword in ['problem', 'issue', 'solve', 'fix']):
            return f"I'll help you address this issue: {user_input}. Let me coordinate with our planning and questioning agents to develop a comprehensive solution."
        
        # General requests
        else:
            return f"I'll help you with: {user_input}. Let me coordinate with the appropriate agents to provide a comprehensive response."
    
    def get_agent_info(self) -> Dict[str, Any]:
        """
        Get agent information and capabilities.
        
        Returns:
            Dict[str, Any]: Agent information
        """
        return {
            'agent_name': self.agent_name,
            'version': self.version,
            'capabilities': [
                'User input processing',
                'Initial response generation',
                'Request categorization',
                'Agent coordination initiation'
            ],
            'input_format': 'Natural language text',
            'output_format': 'Structured JSON (albert_core_schema)'
        } 