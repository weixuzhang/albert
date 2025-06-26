import unittest
import json
from questioning_agent import QuestioningAgent


class TestQuestioningAgent(unittest.TestCase):
    
    def setUp(self):
        self.questioner = QuestioningAgent()
    
    def test_refine_plan_returns_json(self):
        """Test that Questioning Agent returns structured JSON with refined plan"""
        plan_output = {
            'agent_type': 'planning_agent',
            'plan_id': 'plan_001',
            'tasks': [
                {
                    'task_id': 'task_001',
                    'description': 'Organize conference',
                    'priority': 'high',
                    'status': 'pending'
                }
            ],
            'timestamp': '2024-01-01T10:00:00Z'
        }
        
        result = self.questioner.refine_plan(plan_output)
        
        # Should return a dictionary with refined plan structure
        self.assertIsInstance(result, dict)
        self.assertIn('agent_type', result)
        self.assertIn('refined_plan', result)
        self.assertIn('questions', result)
        self.assertIn('missing_details', result)
        self.assertIn('timestamp', result)
        self.assertEqual(result['agent_type'], 'questioning_agent')
    
    def test_identify_missing_details(self):
        """Test that agent identifies missing or ambiguous details"""
        plan_output = {
            'agent_type': 'planning_agent',
            'plan_id': 'plan_001',
            'tasks': [
                {
                    'task_id': 'task_001',
                    'description': 'Vague task description',
                    'priority': 'high',
                    'status': 'pending'
                }
            ],
            'timestamp': '2024-01-01T10:00:00Z'
        }
        
        result = self.questioner.refine_plan(plan_output)
        
        # Should identify missing details
        self.assertIsInstance(result['missing_details'], list)
        self.assertIsInstance(result['questions'], list)
        
        # Should have some missing details for vague task
        self.assertGreater(len(result['missing_details']), 0)
    
    def test_json_serialization(self):
        """Test that refined plan output can be serialized to JSON"""
        plan_output = {
            'agent_type': 'planning_agent',
            'plan_id': 'plan_001',
            'tasks': [
                {
                    'task_id': 'task_001',
                    'description': 'Test task',
                    'priority': 'medium',
                    'status': 'pending'
                }
            ],
            'timestamp': '2024-01-01T10:00:00Z'
        }
        
        result = self.questioner.refine_plan(plan_output)
        json_str = json.dumps(result)
        self.assertIsInstance(json_str, str)


if __name__ == '__main__':
    unittest.main() 