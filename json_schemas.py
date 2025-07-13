"""
JSON Schema definitions for AI Agent Sandbox Prototype
Defines standard structures for agent outputs and inter-agent communication.
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import uuid


class JSONSchemas:
    """Standard JSON schemas for agent outputs with validation"""
    
    @staticmethod
    def validate_json_structure(data: Any, expected_fields: List[str] = None) -> Dict[str, Any]:
        """
        Validate JSON structure and sanitize data
        
        Args:
            data: Data to validate
            expected_fields: List of expected field names
            
        Returns:
            Dict with validation result and cleaned data
        """
        
        if data is None:
            return {'valid': False, 'error': 'Data is None', 'data': None}
        
        # Ensure data is serializable
        try:
            json.dumps(data)
        except (TypeError, ValueError) as e:
            logging.warning(f"JSON serialization failed: {e}")
            return {'valid': False, 'error': f'Data not serializable: {e}', 'data': None}
        
        # Check expected fields if provided
        if expected_fields and isinstance(data, dict):
            missing_fields = [field for field in expected_fields if field not in data]
            if missing_fields:
                logging.warning(f"Missing expected fields: {missing_fields}")
        
        return {'valid': True, 'error': None, 'data': data}
    
    @staticmethod
    def safe_json_loads(json_str: str) -> Dict[str, Any]:
        """
        Safely parse JSON string with error handling
        
        Args:
            json_str: JSON string to parse
            
        Returns:
            Parsed JSON or error structure
        """
        
        if not isinstance(json_str, str):
            return {'error': 'Input is not a string', 'data': None}
        
        try:
            return {'error': None, 'data': json.loads(json_str)}
        except json.JSONDecodeError as e:
            logging.error(f"JSON parsing failed: {e}")
            return {'error': f'JSON parsing failed: {e}', 'data': None}
        except Exception as e:
            logging.error(f"Unexpected error parsing JSON: {e}")
            return {'error': f'Unexpected error: {e}', 'data': None}
    
    @staticmethod
    def get_timestamp() -> str:
        """Generate ISO format timestamp"""
        return datetime.utcnow().isoformat() + 'Z'
    
    @staticmethod
    def generate_id(prefix: str) -> str:
        """Generate unique ID with prefix"""
        return f"{prefix}_{uuid.uuid4().hex[:8]}"
    
    @staticmethod
    def albert_core_schema(user_input: str, response: str, error: Optional[str] = None) -> Dict[str, Any]:
        """Schema for Albert Core agent output with validation"""
        
        # Sanitize inputs
        user_input = str(user_input) if user_input is not None else ""
        response = str(response) if response is not None else ""
        
        schema = {
            'agent_type': 'albert_core',
            'user_input': user_input[:1000],  # Limit length
            'response': response[:5000],  # Limit length
            'timestamp': JSONSchemas.get_timestamp()
        }
        
        if error is not None:
            schema['error'] = str(error)[:500]  # Limit error message length
        
        # Validate structure
        validation = JSONSchemas.validate_json_structure(
            schema, ['agent_type', 'user_input', 'response', 'timestamp']
        )
        
        if not validation['valid']:
            logging.error(f"Albert Core schema validation failed: {validation['error']}")
            
        return schema
    
    @staticmethod
    def planning_agent_schema(plan_id: str, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Schema for Planning Agent output"""
        return {
            'agent_type': 'planning_agent',
            'plan_id': plan_id,
            'tasks': tasks,
            'timestamp': JSONSchemas.get_timestamp()
        }
    
    @staticmethod
    def task_schema(task_id: str, description: str, priority: str = 'medium', 
                   status: str = 'pending', details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Schema for individual task within a plan with validation"""
        
        # Validate and sanitize inputs
        valid_priorities = ['high', 'medium', 'low']
        valid_statuses = ['pending', 'in_progress', 'completed', 'blocked']
        
        task: Dict[str, Any] = {
            'task_id': str(task_id),
            'description': str(description)[:500],  # Limit description length
            'priority': priority if priority in valid_priorities else 'medium',
            'status': status if status in valid_statuses else 'pending'
        }
        
        if details is not None and isinstance(details, dict):
            # Validate details structure
            validated_details = JSONSchemas.validate_json_structure(details)
            if validated_details['valid']:
                task['details'] = details
            else:
                logging.warning(f"Invalid task details: {validated_details['error']}")
                task['details'] = {}
        
        return task
    
    @staticmethod
    def questioning_agent_schema(refined_plan: Dict[str, Any], questions: List[str], 
                               missing_details: List[str]) -> Dict[str, Any]:
        """Schema for Questioning Agent output"""
        return {
            'agent_type': 'questioning_agent',
            'refined_plan': refined_plan,
            'questions': questions,
            'missing_details': missing_details,
            'timestamp': JSONSchemas.get_timestamp()
        }
    
    @staticmethod
    def orchestrator_schema(orchestrator_id: str, user_input: str, 
                          albert_output: Dict[str, Any], planning_output: Dict[str, Any],
                          questioning_output: Dict[str, Any], final_result: Dict[str, Any]) -> Dict[str, Any]:
        """Schema for Orchestrator consolidated output"""
        return {
            'orchestrator_id': orchestrator_id,
            'user_input': user_input,
            'albert_output': albert_output,
            'planning_output': planning_output,
            'questioning_output': questioning_output,
            'final_result': final_result,
            'timestamp': JSONSchemas.get_timestamp()
        }
    
    @staticmethod
    def final_result_schema(summary: str, action_plan: List[Dict[str, Any]], 
                          recommendations: Optional[List[str]] = None) -> Dict[str, Any]:
        """Schema for final consolidated result"""
        result = {
            'summary': summary,
            'action_plan': action_plan
        }
        
        if recommendations:
            result['recommendations'] = recommendations
            
        return result 