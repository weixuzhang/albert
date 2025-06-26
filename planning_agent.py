"""
Planning Agent - Strategic plan formulation
Analyzes Albert Core's output and creates structured plans detailing step-by-step processes.
Enhanced with OpenAI GPT-4 capabilities for intelligent planning.
"""

from typing import Dict, Any, List
from json_schemas import JSONSchemas
from config import Config, AgentPrompts
from openai_utils import get_ai_response
import re
import json


class PlanningAgent:
    """
    Planning Agent creates strategic plans based on Albert Core's initial processing.
    Generates structured, step-by-step task breakdowns.
    """
    
    def __init__(self):
        """Initialize Planning Agent"""
        self.agent_name = "Planning Agent"
        self.version = "1.0.0"
    
    def create_plan(self, albert_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create structured plan based on Albert Core's output.
        Uses OpenAI GPT-4 if available, falls back to rule-based planning otherwise.
        
        Args:
            albert_output (Dict[str, Any]): Output from Albert Core agent
            
        Returns:
            Dict[str, Any]: Structured plan following planning_agent_schema
        """
        
        # Generate unique plan ID
        plan_id = JSONSchemas.generate_id("plan")
        
        # Extract user intent and response from Albert's output
        user_input = albert_output.get('user_input', '')
        albert_response = albert_output.get('response', '')
        
        # Try to use OpenAI API if enabled and configured
        if Config.ENABLE_AI_AGENTS:
            ai_tasks = self._generate_ai_tasks(user_input, albert_response)
            if ai_tasks:
                return JSONSchemas.planning_agent_schema(
                    plan_id=plan_id,
                    tasks=ai_tasks
                )
        
        # Fallback to simple rule-based task generation
        if Config.FALLBACK_TO_SIMPLE_AGENTS:
            simple_tasks = self._generate_simple_tasks(user_input, albert_response)
            return JSONSchemas.planning_agent_schema(
                plan_id=plan_id,
                tasks=simple_tasks
            )
        
        # Return empty plan if both methods fail
        return JSONSchemas.planning_agent_schema(
            plan_id=plan_id,
            tasks=[]
        )
    
    def _generate_ai_tasks(self, user_input: str, albert_response: str) -> List[Dict[str, Any]]:
        """
        Generate task list using OpenAI GPT-4
        
        Args:
            user_input (str): Original user input
            albert_response (str): Albert Core's response
            
        Returns:
            List[Dict[str, Any]]: List of AI-generated structured tasks
        """
        
        try:
            messages = [
                {
                    "role": "user",
                    "content": f"""
User Request: {user_input}
Albert's Initial Response: {albert_response}

Please create a detailed plan with 3-6 specific, actionable tasks. For each task, provide:
- Clear, specific description
- Priority level (high/medium/low)
- Category (planning/problem_solving/project/event/general)
- Realistic time estimate
- Any special details or requirements

Focus on practical, executable tasks that directly address the user's needs.
                    """
                }
            ]
            
            expected_fields = ['tasks', 'plan_summary']
            ai_response = get_ai_response(
                messages=messages,
                system_prompt=AgentPrompts.PLANNING_AGENT_SYSTEM_PROMPT,
                expected_fields=expected_fields
            )
            
            if isinstance(ai_response, dict) and 'tasks' in ai_response:
                return self._process_ai_tasks(ai_response['tasks'])
            elif isinstance(ai_response, str):
                # Try to extract tasks from text response
                return self._extract_tasks_from_text(ai_response)
                
        except Exception as e:
            print(f"⚠️  Planning Agent AI response failed: {e}")
        
        return []
    
    def _process_ai_tasks(self, ai_tasks: Any) -> List[Dict[str, Any]]:
        """Process AI-generated tasks into our standard format"""
        
        processed_tasks = []
        
        if isinstance(ai_tasks, list):
            for task in ai_tasks:
                if isinstance(task, dict):
                    processed_task = JSONSchemas.task_schema(
                        task_id=JSONSchemas.generate_id("task"),
                        description=task.get('description', 'AI-generated task'),
                        priority=task.get('priority', 'medium'),
                        details={
                            'category': task.get('category', 'general'),
                            'estimated_time': task.get('estimated_time', 'varies'),
                            'ai_generated': True
                        }
                    )
                    processed_tasks.append(processed_task)
                elif isinstance(task, str):
                    # Simple string task
                    processed_task = JSONSchemas.task_schema(
                        task_id=JSONSchemas.generate_id("task"),
                        description=task,
                        priority='medium',
                        details={
                            'category': 'general',
                            'estimated_time': 'varies',
                            'ai_generated': True
                        }
                    )
                    processed_tasks.append(processed_task)
        
        return processed_tasks
    
    def _extract_tasks_from_text(self, text_response: str) -> List[Dict[str, Any]]:
        """Extract tasks from AI text response"""
        
        tasks = []
        lines = text_response.split('\n')
        
        for line in lines:
            line = line.strip()
            if line and (line.startswith('-') or line.startswith('•') or line.startswith('*')):
                task_description = line.lstrip('-•* ').strip()
                if task_description:
                    task = JSONSchemas.task_schema(
                        task_id=JSONSchemas.generate_id("task"),
                        description=task_description,
                        priority='medium',
                        details={
                            'category': 'general',
                            'estimated_time': 'varies',
                            'ai_generated': True
                        }
                    )
                    tasks.append(task)
        
        return tasks if tasks else self._create_default_ai_tasks()
    
    def _create_default_ai_tasks(self) -> List[Dict[str, Any]]:
        """Create default tasks when AI response parsing fails"""
        
        return [
            JSONSchemas.task_schema(
                task_id=JSONSchemas.generate_id("task"),
                description="Analyze and define project requirements",
                priority="high",
                details={'category': 'general', 'estimated_time': '1-2 hours', 'ai_generated': False}
            ),
            JSONSchemas.task_schema(
                task_id=JSONSchemas.generate_id("task"),
                description="Research and gather necessary resources",
                priority="medium",
                details={'category': 'general', 'estimated_time': '1 hour', 'ai_generated': False}
            ),
            JSONSchemas.task_schema(
                task_id=JSONSchemas.generate_id("task"),
                description="Execute planned activities",
                priority="medium",
                details={'category': 'general', 'estimated_time': 'varies', 'ai_generated': False}
            )
        ]
    
    def _generate_simple_tasks(self, user_input: str, albert_response: str) -> List[Dict[str, Any]]:
        """
        Generate task list based on user input and Albert's response.
        
        Args:
            user_input (str): Original user input
            albert_response (str): Albert Core's response
            
        Returns:
            List[Dict[str, Any]]: List of structured tasks
        """
        
        tasks = []
        input_lower = user_input.lower()
        
        # Planning-related tasks
        if any(keyword in input_lower for keyword in ['plan', 'organize', 'schedule']):
            tasks.extend(self._create_planning_tasks(user_input))
        
        # Problem-solving tasks
        elif any(keyword in input_lower for keyword in ['problem', 'issue', 'solve', 'fix']):
            tasks.extend(self._create_problem_solving_tasks(user_input))
        
        # Project-related tasks
        elif any(keyword in input_lower for keyword in ['project', 'build', 'create', 'develop']):
            tasks.extend(self._create_project_tasks(user_input))
        
        # Event-related tasks
        elif any(keyword in input_lower for keyword in ['event', 'meeting', 'conference', 'workshop']):
            tasks.extend(self._create_event_tasks(user_input))
        
        # General tasks
        else:
            tasks.extend(self._create_general_tasks(user_input))
        
        return tasks
    
    def _create_planning_tasks(self, user_input: str) -> List[Dict[str, Any]]:
        """Create planning-specific tasks"""
        return [
            JSONSchemas.task_schema(
                task_id=JSONSchemas.generate_id("task"),
                description="Define project scope and objectives",
                priority="high",
                details={"category": "planning", "estimated_time": "1-2 hours"}
            ),
            JSONSchemas.task_schema(
                task_id=JSONSchemas.generate_id("task"),
                description="Identify required resources and constraints",
                priority="high",
                details={"category": "planning", "estimated_time": "30-60 minutes"}
            ),
            JSONSchemas.task_schema(
                task_id=JSONSchemas.generate_id("task"),
                description="Create timeline and milestones",
                priority="medium",
                details={"category": "planning", "estimated_time": "1 hour"}
            ),
            JSONSchemas.task_schema(
                task_id=JSONSchemas.generate_id("task"),
                description="Assign responsibilities and roles",
                priority="medium",
                details={"category": "planning", "estimated_time": "30 minutes"}
            )
        ]
    
    def _create_problem_solving_tasks(self, user_input: str) -> List[Dict[str, Any]]:
        """Create problem-solving specific tasks"""
        return [
            JSONSchemas.task_schema(
                task_id=JSONSchemas.generate_id("task"),
                description="Analyze and define the problem clearly",
                priority="high",
                details={"category": "problem_solving", "estimated_time": "30-60 minutes"}
            ),
            JSONSchemas.task_schema(
                task_id=JSONSchemas.generate_id("task"),
                description="Research potential solutions and approaches",
                priority="high",
                details={"category": "problem_solving", "estimated_time": "1-2 hours"}
            ),
            JSONSchemas.task_schema(
                task_id=JSONSchemas.generate_id("task"),
                description="Evaluate and select best solution approach",
                priority="medium",
                details={"category": "problem_solving", "estimated_time": "45 minutes"}
            ),
            JSONSchemas.task_schema(
                task_id=JSONSchemas.generate_id("task"),
                description="Implement solution and monitor results",
                priority="medium",
                details={"category": "problem_solving", "estimated_time": "varies"}
            )
        ]
    
    def _create_project_tasks(self, user_input: str) -> List[Dict[str, Any]]:
        """Create project-specific tasks"""
        return [
            JSONSchemas.task_schema(
                task_id=JSONSchemas.generate_id("task"),
                description="Define project requirements and specifications",
                priority="high",
                details={"category": "project", "estimated_time": "2-3 hours"}
            ),
            JSONSchemas.task_schema(
                task_id=JSONSchemas.generate_id("task"),
                description="Design project architecture and structure",
                priority="high",
                details={"category": "project", "estimated_time": "1-2 hours"}
            ),
            JSONSchemas.task_schema(
                task_id=JSONSchemas.generate_id("task"),
                description="Implement core functionality",
                priority="medium",
                details={"category": "project", "estimated_time": "varies"}
            ),
            JSONSchemas.task_schema(
                task_id=JSONSchemas.generate_id("task"),
                description="Test and validate implementation",
                priority="medium",
                details={"category": "project", "estimated_time": "1-2 hours"}
            )
        ]
    
    def _create_event_tasks(self, user_input: str) -> List[Dict[str, Any]]:
        """Create event-specific tasks"""
        return [
            JSONSchemas.task_schema(
                task_id=JSONSchemas.generate_id("task"),
                description="Define event purpose and target audience",
                priority="high",
                details={"category": "event", "estimated_time": "1 hour"}
            ),
            JSONSchemas.task_schema(
                task_id=JSONSchemas.generate_id("task"),
                description="Plan event logistics and venue requirements",
                priority="high",
                details={"category": "event", "estimated_time": "2-3 hours"}
            ),
            JSONSchemas.task_schema(
                task_id=JSONSchemas.generate_id("task"),
                description="Coordinate speakers, materials, and resources",
                priority="medium",
                details={"category": "event", "estimated_time": "varies"}
            ),
            JSONSchemas.task_schema(
                task_id=JSONSchemas.generate_id("task"),
                description="Execute event and gather feedback",
                priority="low",
                details={"category": "event", "estimated_time": "event duration + 1 hour"}
            )
        ]
    
    def _create_general_tasks(self, user_input: str) -> List[Dict[str, Any]]:
        """Create general tasks for unspecified requests"""
        return [
            JSONSchemas.task_schema(
                task_id=JSONSchemas.generate_id("task"),
                description=f"Analyze request: {user_input}",
                priority="high",
                details={"category": "general", "estimated_time": "30 minutes"}
            ),
            JSONSchemas.task_schema(
                task_id=JSONSchemas.generate_id("task"),
                description="Research relevant information and best practices",
                priority="medium",
                details={"category": "general", "estimated_time": "1-2 hours"}
            ),
            JSONSchemas.task_schema(
                task_id=JSONSchemas.generate_id("task"),
                description="Develop actionable recommendations",
                priority="medium",
                details={"category": "general", "estimated_time": "45 minutes"}
            )
        ]
    
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
                'Strategic plan creation',
                'Task breakdown and prioritization',
                'Resource estimation',
                'Timeline planning'
            ],
            'input_format': 'Albert Core JSON output',
            'output_format': 'Structured JSON (planning_agent_schema)'
        } 