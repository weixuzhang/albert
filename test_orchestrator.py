import unittest
import json
from orchestrator import Orchestrator


class TestOrchestrator(unittest.TestCase):
    
    def setUp(self):
        self.orchestrator = Orchestrator()
    
    def test_process_user_request_returns_json(self):
        """Test that Orchestrator coordinates agents and returns final JSON"""
        user_input = "I need help planning a team building event"
        
        result = self.orchestrator.process_user_request(user_input)
        
        # Should return consolidated output from all agents
        self.assertIsInstance(result, dict)
        self.assertIn('orchestrator_id', result)
        self.assertIn('user_input', result)
        self.assertIn('albert_output', result)
        self.assertIn('planning_output', result)
        self.assertIn('questioning_output', result)
        self.assertIn('final_result', result)
        self.assertIn('timestamp', result)
    
    def test_agent_communication_flow(self):
        """Test that agents communicate properly through orchestrator"""
        user_input = "Simple test request"
        
        result = self.orchestrator.process_user_request(user_input)
        
        # Verify the flow: Albert -> Planning -> Questioning
        self.assertEqual(result['albert_output']['agent_type'], 'albert_core')
        self.assertEqual(result['planning_output']['agent_type'], 'planning_agent')
        self.assertEqual(result['questioning_output']['agent_type'], 'questioning_agent')
    
    def test_json_yaml_ready_output(self):
        """Test that final output is structured for YAML conversion"""
        user_input = "Test for YAML conversion"
        
        result = self.orchestrator.process_user_request(user_input)
        
        # Should be serializable to JSON
        json_str = json.dumps(result)
        self.assertIsInstance(json_str, str)
        
        # Should have clean structure for YAML conversion
        self.assertIn('final_result', result)
        final_result = result['final_result']
        self.assertIn('summary', final_result)
        self.assertIn('action_plan', final_result)


if __name__ == '__main__':
    unittest.main() 