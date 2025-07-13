"""
Questioning Agent (Slot Filler) - Clarification and information augmentation
Reviews and refines plans from the Planning Agent, identifies missing or ambiguous details.
Enhanced with OpenAI GPT-4 capabilities for intelligent question generation.
"""

from typing import Dict, Any, List, Optional
from json_schemas import JSONSchemas
from config import Config, AgentPrompts
from openai_utils import get_ai_response
import re
import json


class QuestioningAgent:
    """
    Questioning Agent reviews plans and identifies missing or ambiguous details.
    Acts as a slot-filler to ensure plans are complete and actionable.
    """
    
    def __init__(self):
        """Initialize Questioning Agent"""
        self.agent_name = "Questioning Agent"
        self.version = "1.0.0"
        
        # Define required slots/details for different task categories
        self.required_slots = {
            'planning': ['timeline', 'resources', 'stakeholders', 'success_criteria'],
            'problem_solving': ['problem_definition', 'constraints', 'success_metrics', 'alternatives'],
            'project': ['requirements', 'deliverables', 'timeline', 'budget', 'team'],
            'event': ['date', 'location', 'attendees', 'agenda', 'budget'],
            'general': ['objectives', 'constraints', 'success_criteria']
        }
    
    def refine_plan(self, plan_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Refine plan by identifying missing details and generating clarifying questions.
        Uses OpenAI GPT-4 if available, falls back to rule-based analysis otherwise.
        
        Args:
            plan_output (Dict[str, Any]): Output from Planning Agent
            
        Returns:
            Dict[str, Any]: Refined plan with questions and missing details
        """
        
        # Extract plan details
        tasks = plan_output.get('tasks', [])
        plan_id = plan_output.get('plan_id', 'unknown')
        
        # Try to use OpenAI API if enabled and configured
        if Config.ENABLE_AI_AGENTS:
            ai_analysis = self._get_ai_analysis(plan_output)
            if ai_analysis:
                return ai_analysis
        
        # Fallback to simple rule-based analysis
        if Config.FALLBACK_TO_SIMPLE_AGENTS:
            # Analyze tasks for missing details
            missing_details = self._identify_missing_details_simple(tasks)
            
            # Generate clarifying questions
            questions = self._generate_questions_simple(tasks, missing_details)
            
            # Create refined plan with additional details
            refined_plan = self._create_refined_plan(plan_output, missing_details)
            
            # Return structured questioning output
            return JSONSchemas.questioning_agent_schema(
                refined_plan=refined_plan,
                questions=questions,
                missing_details=missing_details
            )
        
        # Return basic response if both methods fail
        return JSONSchemas.questioning_agent_schema(
            refined_plan=plan_output,
            questions=[],
            missing_details=[]
        )
    
    def _get_ai_analysis(self, plan_output: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Get AI-powered analysis of the plan to identify missing details and generate questions
        
        Args:
            plan_output (Dict[str, Any]): Plan from Planning Agent
            
        Returns:
            Dict[str, Any]: Complete questioning agent output or None if failed
        """
        
        try:
            plan_summary = json.dumps(plan_output, indent=2)
            
            messages = [
                {
                    "role": "user",
                    "content": f"""
Analyze this plan and identify what information is missing or unclear:

{plan_summary}

Please provide:
1. A list of specific missing details or information gaps
2. 3-8 clarifying questions that would help make this plan more complete and actionable
3. A completeness score (0-1) for the current plan
4. Specific suggestions for improvement

Focus on practical details needed for successful execution.
                    """
                }
            ]
            
            expected_fields = ['missing_details', 'questions', 'completeness_score', 'suggestions']
            ai_response = get_ai_response(
                messages=messages,
                system_prompt=AgentPrompts.QUESTIONING_AGENT_SYSTEM_PROMPT,
                expected_fields=expected_fields
            )
            
            if isinstance(ai_response, dict):
                return self._process_ai_analysis(plan_output, ai_response)
            elif isinstance(ai_response, str):
                return self._extract_analysis_from_text(plan_output, ai_response)
                
        except Exception as e:
            print(f"[WARNING] Questioning Agent AI analysis failed: {e}")
        
        return None
    
    def _process_ai_analysis(self, plan_output: Dict[str, Any], ai_response: Dict[str, Any]) -> Dict[str, Any]:
        """Process AI analysis response into standard format"""
        
        # Extract data from AI response
        missing_details = ai_response.get('missing_details', [])
        questions = ai_response.get('questions', [])
        completeness_score = ai_response.get('completeness_score', 0.5)
        suggestions = ai_response.get('suggestions', [])
        
        # Ensure lists are actually lists
        if not isinstance(missing_details, list):
            missing_details = [str(missing_details)]
        if not isinstance(questions, list):
            questions = [str(questions)]
        if not isinstance(suggestions, list):
            suggestions = [str(suggestions)]
        
        # Create refined plan
        refined_plan = plan_output.copy()
        refined_plan['refinement_status'] = 'ai_reviewed'
        refined_plan['missing_details_count'] = len(missing_details)
        refined_plan['completeness_score'] = float(completeness_score) if isinstance(completeness_score, (int, float)) else 0.5
        refined_plan['improvement_suggestions'] = suggestions
        refined_plan['ai_analysis'] = True
        
        return JSONSchemas.questioning_agent_schema(
            refined_plan=refined_plan,
            questions=questions,
            missing_details=missing_details
        )
    
    def _extract_analysis_from_text(self, plan_output: Dict[str, Any], text_response: str) -> Dict[str, Any]:
        """Extract analysis from AI text response"""
        
        missing_details = []
        questions = []
        
        lines = text_response.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Detect sections
            if 'missing' in line.lower() or 'gap' in line.lower():
                current_section = 'missing'
                continue
            elif 'question' in line.lower():
                current_section = 'questions'
                continue
            
            # Extract content
            if line.startswith(('-', '•', '*', '1.', '2.', '3.', '4.', '5.')):
                content = line.split('.', 1)[-1].strip().lstrip('-•* ')
                if current_section == 'missing':
                    missing_details.append(content)
                elif current_section == 'questions':
                    questions.append(content)
        
        # Create refined plan
        refined_plan = plan_output.copy()
        refined_plan['refinement_status'] = 'ai_reviewed'
        refined_plan['missing_details_count'] = len(missing_details)
        refined_plan['completeness_score'] = 0.6  # Default score
        refined_plan['improvement_suggestions'] = ['Review AI-generated analysis for detailed recommendations']
        refined_plan['ai_analysis'] = True
        
        return JSONSchemas.questioning_agent_schema(
            refined_plan=refined_plan,
            questions=questions if questions else ['What additional details would help make this plan more specific?'],
            missing_details=missing_details if missing_details else ['More specific requirements and constraints needed']
        )
    
    def _identify_missing_details_simple(self, tasks: List[Dict[str, Any]]) -> List[str]:
        """
        Identify missing details across all tasks.
        
        Args:
            tasks (List[Dict[str, Any]]): List of tasks from planning agent
            
        Returns:
            List[str]: List of missing detail descriptions
        """
        
        missing_details = []
        
        for task in tasks:
            task_details = task.get('details', {})
            category = task_details.get('category', 'general')
            description = task.get('description', '')
            
            # Check for required slots based on category
            required_slots = self.required_slots.get(category, self.required_slots['general'])
            
            # Check for missing timeline details
            if 'timeline' in required_slots and not self._has_timeline_details(task_details):
                missing_details.append(f"Specific timeline/deadline for task: {description}")
            
            # Check for missing resource details
            if 'resources' in required_slots and not self._has_resource_details(task_details):
                missing_details.append(f"Required resources for task: {description}")
            
            # Check for missing stakeholder details
            if 'stakeholders' in required_slots and not self._has_stakeholder_details(task_details):
                missing_details.append(f"Responsible parties/stakeholders for task: {description}")
            
            # Check for missing success criteria
            if 'success_criteria' in required_slots and not self._has_success_criteria(task_details):
                missing_details.append(f"Success criteria/acceptance criteria for task: {description}")
            
            # Check for vague or incomplete descriptions
            if self._is_description_vague(description):
                missing_details.append(f"More specific details needed for task: {description}")
        
        return missing_details
    
    def _generate_questions_simple(self, tasks: List[Dict[str, Any]], missing_details: List[str]) -> List[str]:
        """
        Generate clarifying questions based on missing details.
        
        Args:
            tasks (List[Dict[str, Any]]): List of tasks
            missing_details (List[str]): List of missing details
            
        Returns:
            List[str]: List of clarifying questions
        """
        
        questions = []
        
        # Generate questions for missing details
        for detail in missing_details:
            if 'timeline' in detail.lower():
                questions.append("What is the specific deadline or timeline for this task?")
            elif 'resource' in detail.lower():
                questions.append("What resources (people, tools, budget) are needed for this task?")
            elif 'stakeholder' in detail.lower():
                questions.append("Who is responsible for completing this task?")
            elif 'success criteria' in detail.lower():
                questions.append("How will you know when this task is successfully completed?")
            elif 'specific details' in detail.lower():
                questions.append("Can you provide more specific details about what needs to be done?")
        
        # Generate category-specific questions
        categories = set()
        for task in tasks:
            category = task.get('details', {}).get('category', 'general')
            categories.add(category)
        
        for category in categories:
            questions.extend(self._get_category_specific_questions(category))
        
        # Remove duplicates and limit to most important questions
        questions = list(set(questions))[:10]  # Limit to top 10 questions
        
        return questions
    
    def _create_refined_plan(self, original_plan: Dict[str, Any], missing_details: List[str]) -> Dict[str, Any]:
        """
        Create refined plan with suggested improvements.
        
        Args:
            original_plan (Dict[str, Any]): Original plan from Planning Agent
            missing_details (List[str]): Identified missing details
            
        Returns:
            Dict[str, Any]: Refined plan with improvements
        """
        
        refined_plan = original_plan.copy()
        
        # Add refinement metadata
        refined_plan['refinement_status'] = 'reviewed'
        refined_plan['missing_details_count'] = len(missing_details)
        refined_plan['completeness_score'] = self._calculate_completeness_score(original_plan, missing_details)
        
        # Add suggestions for improvement
        refined_plan['improvement_suggestions'] = self._generate_improvement_suggestions(missing_details)
        
        return refined_plan
    
    def _has_timeline_details(self, task_details: Dict[str, Any]) -> bool:
        """Check if task has specific timeline details"""
        estimated_time = task_details.get('estimated_time', '')
        return estimated_time and 'varies' not in estimated_time.lower()
    
    def _has_resource_details(self, task_details: Dict[str, Any]) -> bool:
        """Check if task has resource details"""
        return 'resources' in task_details or 'budget' in task_details
    
    def _has_stakeholder_details(self, task_details: Dict[str, Any]) -> bool:
        """Check if task has stakeholder details"""
        return 'assignee' in task_details or 'responsible_party' in task_details
    
    def _has_success_criteria(self, task_details: Dict[str, Any]) -> bool:
        """Check if task has success criteria"""
        return 'success_criteria' in task_details or 'acceptance_criteria' in task_details
    
    def _is_description_vague(self, description: str) -> bool:
        """Check if task description is vague or incomplete"""
        vague_indicators = ['organize', 'plan', 'coordinate', 'manage', 'handle', 'deal with']
        return any(indicator in description.lower() for indicator in vague_indicators) and len(description.split()) < 5
    
    def _get_category_specific_questions(self, category: str) -> List[str]:
        """Get category-specific clarifying questions"""
        category_questions = {
            'planning': [
                "What is the overall budget for this plan?",
                "Who are the key stakeholders that need to be involved?"
            ],
            'problem_solving': [
                "What is the root cause of this problem?",
                "What constraints do we need to work within?"
            ],
            'project': [
                "What are the specific deliverables expected?",
                "What is the project scope and what is out of scope?"
            ],
            'event': [
                "When and where will this event take place?",
                "How many people are expected to attend?"
            ],
            'general': [
                "What is the primary objective of this request?",
                "Are there any specific constraints or requirements?"
            ]
        }
        
        return category_questions.get(category, [])
    
    def _calculate_completeness_score(self, plan: Dict[str, Any], missing_details: List[str]) -> float:
        """Calculate completeness score for the plan (0-1 scale)"""
        total_tasks = len(plan.get('tasks', []))
        if total_tasks == 0:
            return 0.0
        
        # Base score starts at 0.5
        base_score = 0.5
        
        # Deduct points for missing details
        missing_penalty = min(0.4, len(missing_details) * 0.05)
        
        # Add points for well-defined tasks
        well_defined_bonus = 0.1 if total_tasks > 0 else 0
        
        score = base_score - missing_penalty + well_defined_bonus
        return max(0.0, min(1.0, score))
    
    def _generate_improvement_suggestions(self, missing_details: List[str]) -> List[str]:
        """Generate suggestions for plan improvement"""
        suggestions = []
        
        if any('timeline' in detail.lower() for detail in missing_details):
            suggestions.append("Add specific deadlines and time estimates to tasks")
        
        if any('resource' in detail.lower() for detail in missing_details):
            suggestions.append("Identify and document required resources for each task")
        
        if any('stakeholder' in detail.lower() for detail in missing_details):
            suggestions.append("Assign responsible parties for each task")
        
        if any('success criteria' in detail.lower() for detail in missing_details):
            suggestions.append("Define clear success criteria and acceptance criteria")
        
        if len(missing_details) > 5:
            suggestions.append("Consider breaking down complex tasks into smaller, more specific sub-tasks")
        
        return suggestions
    
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
                'Plan refinement and validation',
                'Missing detail identification',
                'Clarifying question generation',
                'Completeness scoring',
                'Improvement suggestions'
            ],
            'input_format': 'Planning Agent JSON output',
            'output_format': 'Structured JSON (questioning_agent_schema)'
        } 