"""
Orchestrator - Central coordinator for AI Agent Sandbox
Manages interactions between agents and consolidates outputs into structured JSON.
"""

from typing import Dict, Any
from json_schemas import JSONSchemas
from albert_core import AlbertCore
from planning_agent import PlanningAgent
from questioning_agent import QuestioningAgent


class Orchestrator:
    """
    Orchestrator coordinates all agent interactions and consolidates outputs.
    Acts as the central coordinator for the AI Agent Sandbox system.
    """
    
    def __init__(self):
        """Initialize Orchestrator with all agents"""
        self.orchestrator_name = "AI Agent Sandbox Orchestrator"
        self.version = "1.0.0"
        
        # Initialize all agents
        self.albert_core = AlbertCore()
        self.planning_agent = PlanningAgent()
        self.questioning_agent = QuestioningAgent()
    
    def process_user_request(self, user_input: str) -> Dict[str, Any]:
        """
        Process user request through all agents and return consolidated result.
        
        Args:
            user_input (str): User's input request
            
        Returns:
            Dict[str, Any]: Consolidated output from all agents
        """
        
        # Generate unique orchestrator ID
        orchestrator_id = JSONSchemas.generate_id("orchestrator")
        
        try:
            # Step 1: Process through Albert Core
            albert_output = self.albert_core.process_user_input(user_input)
            
            # Step 2: Create plan through Planning Agent
            planning_output = self.planning_agent.create_plan(albert_output)
            
            # Step 3: Refine plan through Questioning Agent
            questioning_output = self.questioning_agent.refine_plan(planning_output)
            
            # Step 4: Generate final consolidated result
            final_result = self._create_final_result(
                albert_output, planning_output, questioning_output
            )
            
            # Return consolidated orchestrator output
            return JSONSchemas.orchestrator_schema(
                orchestrator_id=orchestrator_id,
                user_input=user_input,
                albert_output=albert_output,
                planning_output=planning_output,
                questioning_output=questioning_output,
                final_result=final_result
            )
            
        except Exception as e:
            # Handle any errors in the agent pipeline
            return self._create_error_response(orchestrator_id, user_input, str(e))
    
    def _create_final_result(self, albert_output: Dict[str, Any], 
                           planning_output: Dict[str, Any], 
                           questioning_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create final consolidated result from all agent outputs.
        
        Args:
            albert_output (Dict[str, Any]): Albert Core output
            planning_output (Dict[str, Any]): Planning Agent output
            questioning_output (Dict[str, Any]): Questioning Agent output
            
        Returns:
            Dict[str, Any]: Final consolidated result
        """
        
        # Extract key information
        user_request = albert_output.get('user_input', '')
        albert_response = albert_output.get('response', '')
        tasks = planning_output.get('tasks', [])
        questions = questioning_output.get('questions', [])
        missing_details = questioning_output.get('missing_details', [])
        refined_plan = questioning_output.get('refined_plan', {})
        
        # Create summary
        summary = self._generate_summary(user_request, albert_response, tasks, questions)
        
        # Create action plan
        action_plan = self._create_action_plan(tasks, questions, missing_details)
        
        # Create recommendations
        recommendations = self._generate_recommendations(refined_plan, questions, missing_details)
        
        return JSONSchemas.final_result_schema(
            summary=summary,
            action_plan=action_plan,
            recommendations=recommendations
        )
    
    def _generate_summary(self, user_request: str, albert_response: str, 
                         tasks: list, questions: list) -> str:
        """Generate executive summary of the processing results"""
        
        task_count = len(tasks)
        question_count = len(questions)
        
        summary = f"Processing completed for request: '{user_request}'. "
        summary += f"Generated {task_count} tasks and identified {question_count} clarifying questions. "
        summary += f"Initial assessment: {albert_response}"
        
        return summary
    
    def _create_action_plan(self, tasks: list, questions: list, missing_details: list) -> list:
        """Create consolidated action plan"""
        
        action_items = []
        
        # Add immediate action to address questions
        if questions:
            action_items.append({
                'action_id': JSONSchemas.generate_id("action"),
                'type': 'clarification',
                'description': 'Address clarifying questions before proceeding',
                'priority': 'high',
                'details': {
                    'questions_count': len(questions),
                    'questions': questions[:3]  # Include top 3 questions
                }
            })
        
        # Add tasks as action items
        for task in tasks:
            action_items.append({
                'action_id': JSONSchemas.generate_id("action"),
                'type': 'task_execution',
                'description': task.get('description', ''),
                'priority': task.get('priority', 'medium'),
                'details': {
                    'task_id': task.get('task_id'),
                    'category': task.get('details', {}).get('category', 'general'),
                    'estimated_time': task.get('details', {}).get('estimated_time', 'unknown')
                }
            })
        
        # Add follow-up action for missing details
        if missing_details:
            action_items.append({
                'action_id': JSONSchemas.generate_id("action"),
                'type': 'detail_gathering',
                'description': 'Gather additional details for complete planning',
                'priority': 'medium',
                'details': {
                    'missing_details_count': len(missing_details),
                    'examples': missing_details[:3]  # Include top 3 missing details
                }
            })
        
        return action_items
    
    def _generate_recommendations(self, refined_plan: Dict[str, Any], 
                                questions: list, missing_details: list) -> list:
        """Generate recommendations for the user"""
        
        recommendations = []
        
        # Get completeness score if available
        completeness_score = refined_plan.get('completeness_score', 0)
        improvement_suggestions = refined_plan.get('improvement_suggestions', [])
        
        # Recommendations based on completeness
        if completeness_score < 0.7:
            recommendations.append(
                "Consider providing more specific details to improve plan completeness"
            )
        
        # Add improvement suggestions
        recommendations.extend(improvement_suggestions)
        
        # Question-based recommendations
        if len(questions) > 5:
            recommendations.append(
                "Break down your request into smaller, more specific components for better planning"
            )
        
        # Missing details recommendations
        if len(missing_details) > 3:
            recommendations.append(
                "Define clear timelines, resources, and success criteria for better execution"
            )
        
        # General recommendations
        recommendations.append(
            "Review the generated questions and provide answers to refine the plan further"
        )
        
        return recommendations
    
    def _create_error_response(self, orchestrator_id: str, user_input: str, error_message: str) -> Dict[str, Any]:
        """Create error response when agent pipeline fails"""
        
        return {
            'orchestrator_id': orchestrator_id,
            'user_input': user_input,
            'error': error_message,
            'status': 'failed',
            'albert_output': None,
            'planning_output': None,
            'questioning_output': None,
            'final_result': {
                'summary': f"Error processing request: {error_message}",
                'action_plan': [],
                'recommendations': [
                    "Please try rephrasing your request",
                    "Ensure your input is clear and specific"
                ]
            },
            'timestamp': JSONSchemas.get_timestamp()
        }
    
    def get_system_info(self) -> Dict[str, Any]:
        """
        Get information about the orchestrator and all agents.
        
        Returns:
            Dict[str, Any]: System information
        """
        
        return {
            'orchestrator_name': self.orchestrator_name,
            'version': self.version,
            'agents': {
                'albert_core': self.albert_core.get_agent_info(),
                'planning_agent': self.planning_agent.get_agent_info(),
                'questioning_agent': self.questioning_agent.get_agent_info()
            },
            'workflow': [
                "1. Albert Core processes user input",
                "2. Planning Agent creates structured plan",
                "3. Questioning Agent refines and validates plan",
                "4. Orchestrator consolidates results"
            ],
            'output_format': 'JSON (ready for YAML conversion)'
        }
    
    def get_agent_status(self) -> Dict[str, Any]:
        """
        Get status of all agents.
        
        Returns:
            Dict[str, Any]: Agent status information
        """
        
        return {
            'orchestrator_status': 'active',
            'agents_status': {
                'albert_core': 'active',
                'planning_agent': 'active',
                'questioning_agent': 'active'
            },
            'last_check': JSONSchemas.get_timestamp()
        } 