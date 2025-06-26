"""
JSON Schema definitions for AI Agent Sandbox Prototype
Defines standard structures for agent outputs and inter-agent communication.
"""

from datetime import datetime
from typing import Dict, List, Any, Optional
import uuid


class JSONSchemas:
    """Standard JSON schemas for agent outputs"""
    
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
        """Schema for Albert Core agent output"""
        schema = {
            'agent_type': 'albert_core',
            'user_input': user_input,
            'response': response,
            'timestamp': JSONSchemas.get_timestamp()
        }
        
        if error is not None:
            schema['error'] = error
            
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
        """Schema for individual task within a plan"""
        task: Dict[str, Any] = {
            'task_id': task_id,
            'description': description,
            'priority': priority,
            'status': status
        }
        
        if details is not None:
            task['details'] = details
            
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