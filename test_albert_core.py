import unittest
import json
from albert_core import AlbertCore


class TestAlbertCore(unittest.TestCase):
    
    def setUp(self):
        self.albert = AlbertCore()
    
    def test_process_user_input_returns_json(self):
        """Test that Albert Core returns structured JSON output"""
        user_input = "Hello, I need help with planning a project"
        result = self.albert.process_user_input(user_input)
        
        # Should return a dictionary that can be serialized to JSON
        self.assertIsInstance(result, dict)
        self.assertIn('agent_type', result)
        self.assertIn('user_input', result)
        self.assertIn('response', result)
        self.assertIn('timestamp', result)
        self.assertEqual(result['agent_type'], 'albert_core')
    
    def test_process_empty_input(self):
        """Test Albert Core handles empty input gracefully"""
        result = self.albert.process_user_input("")
        
        self.assertIsInstance(result, dict)
        self.assertIn('error', result)
    
    def test_json_serialization(self):
        """Test that output can be serialized to JSON"""
        user_input = "Test input"
        result = self.albert.process_user_input(user_input)
        
        # Should be able to serialize to JSON without errors
        json_str = json.dumps(result)
        self.assertIsInstance(json_str, str)


if __name__ == '__main__':
    unittest.main() 