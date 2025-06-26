import unittest
import json
from planning_agent import PlanningAgent


class TestPlanningAgent(unittest.TestCase):
    
    def setUp(self):
        self.planner = PlanningAgent()
    
    def test_create_plan_returns_json(self):
        """Test that Planning Agent returns structured JSON with plan details"""
        albert_output = {
            'agent_type': 'albert_core',
            'user_input': 'I need to organize a conference',
            'response': 'I can help you organize a conference',
            'timestamp': '2024-01-01T10:00:00Z'
        }
        
        result = self.planner.create_plan(albert_output)
        
        # Should return a dictionary with plan structure
        self.assertIsInstance(result, dict)
        self.assertIn('agent_type', result)
        self.assertIn('plan_id', result)
        self.assertIn('tasks', result)
        self.assertIn('timestamp', result)
        self.assertEqual(result['agent_type'], 'planning_agent')
        self.assertIsInstance(result['tasks'], list)
    
    def test_plan_tasks_structure(self):
        """Test that plan tasks have proper structure"""
        albert_output = {
            'agent_type': 'albert_core',
            'user_input': 'Plan a simple project',
            'response': 'I can help with project planning',
            'timestamp': '2024-01-01T10:00:00Z'
        }
        
        result = self.planner.create_plan(albert_output)
        
        # Each task should have required fields
        for task in result['tasks']:
            self.assertIn('task_id', task)
            self.assertIn('description', task)
            self.assertIn('priority', task)
            self.assertIn('status', task)
    
    def test_json_serialization(self):
        """Test that plan output can be serialized to JSON"""
        albert_output = {
            'agent_type': 'albert_core',
            'user_input': 'Test planning',
            'response': 'Test response',
            'timestamp': '2024-01-01T10:00:00Z'
        }
        
        result = self.planner.create_plan(albert_output)
        json_str = json.dumps(result)
        self.assertIsInstance(json_str, str)


if __name__ == '__main__':
    unittest.main() 