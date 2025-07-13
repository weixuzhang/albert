#!/usr/bin/env python3
"""
AI Agent Sandbox Demo
Run this script to see the system in action.
"""

import logging
import time
from orchestrator import Orchestrator
from config import Config
from openai_utils import check_openai_status
from logger_config import LoggerConfig
import json


def test_simple_use_case():
    """Test a simple birthday party planning request"""
    
    print("AI Agent Sandbox - Enhanced Demo")
    print("=" * 50)
    
    # Initialize logging
    logging.info("Starting AI Agent Sandbox demo")
    
    # Check OpenAI status
    print("[CONFIG] Checking OpenAI Configuration...")
    
    try:
        openai_status = check_openai_status()
        LoggerConfig.log_api_call("OpenAI", "status_check", error=None if openai_status['configured'] else "Not configured")
    except Exception as e:
        logging.error(f"Failed to check OpenAI status: {e}")
        print(f"[ERROR] Failed to check OpenAI status: {e}")
        return False
    
    print(f"[STATUS] API Key: {'Set' if openai_status['api_key_set'] else 'Not Set'}")
    print(f"[STATUS] Model: {openai_status['model']}")
    print(f"[STATUS] Client: {'Configured' if openai_status['configured'] else 'Not Configured'}")
    
    if not openai_status['configured']:
        print("[WARNING] OpenAI not properly configured!")
        print("[INFO] Set your API key: export OPENAI_API_KEY='your-key-here'")
        print("[INFO] Will use fallback agents instead...")
        Config.ENABLE_AI_AGENTS = False
    
    # Test connection
    print("\n[TEST] Testing OpenAI Connection...")
    connection_start = time.time()
    
    if openai_status['connection_test']:
        connection_time = time.time() - connection_start
        LoggerConfig.log_api_call("OpenAI", "connection_test", response_time=connection_time)
        print("[SUCCESS] OpenAI connection successful!")
    else:
        LoggerConfig.log_api_call("OpenAI", "connection_test_failed")
        print("[ERROR] OpenAI connection failed!")
        print("[INFO] Will use fallback agents instead...")
        Config.ENABLE_AI_AGENTS = False
    
    # Initialize orchestrator
    print("\n[INIT] Initializing AI Agents...")
    orchestrator = Orchestrator()
    
    # Test request
    user_request = "I want to plan a birthday party for my 8-year-old daughter. We'll have about 12 kids."
    
    print(f"\n[INPUT] User Request: {user_request}")
    
    try:
        # Process the request
        print("\n[PROCESSING] Processing through agent pipeline...")
        start_time = time.time()
        
        result = orchestrator.process_user_request(user_request)
        
        processing_time = time.time() - start_time
        print(f"[SUCCESS] Processing completed in {processing_time:.2f} seconds")
        
        # Display results
        print("\n" + "="*60)
        print("ALBERT CORE")
        print("="*60)
        albert_response = result['albert_output']['response']
        print(f"Response: {albert_response}")
        
        print("\n" + "="*60)
        print("PLANNING AGENT")
        print("="*60)
        tasks = result['planning_output']['tasks']
        print(f"Generated {len(tasks)} tasks:")
        for i, task in enumerate(tasks[:3], 1):  # Show first 3
            print(f"\n{i}. {task['description']}")
            print(f"   Priority: {task['priority']}")
            print(f"   Category: {task.get('details', {}).get('category', 'N/A')}")
        
        print("\n" + "="*60)
        print("QUESTIONING AGENT")
        print("="*60)
        questions = result['questioning_output']['questions']
        missing_details = result['questioning_output']['missing_details']
        
        print(f"Clarifying Questions ({len(questions)}):")
        for i, question in enumerate(questions[:3], 1):  # Show first 3
            print(f"{i}. {question}")
        
        # Check if AI was used and display metadata
        refined_plan = result['questioning_output']['refined_plan']
        ai_analysis = refined_plan.get('ai_analysis', False)
        completeness_score = refined_plan.get('completeness_score', 0)
        
        metadata = result.get('processing_metadata', {})
        
        print(f"\n[STATUS] AI Analysis Used: {'YES' if ai_analysis else 'NO'}")
        print(f"[METRICS] Plan Completeness Score: {completeness_score:.2f}/1.0")
        print(f"[METRICS] Total Processing Time: {metadata.get('processing_time_seconds', 'N/A')}s")
        
        print("\n" + "="*60)
        print("FINAL RESULT")
        print("="*60)
        final_result = result['final_result']
        print(f"Summary: {final_result['summary']}")
        
        print(f"\nRecommendations ({len(final_result['recommendations'])}):")
        for i, rec in enumerate(final_result['recommendations'][:2], 1):
            print(f"{i}. {rec}")
        
        print("\n[SUCCESS] Demo completed successfully!")
        
        if ai_analysis:
            print("[INFO] All agents are working with OpenAI GPT-4!")
        else:
            print("[INFO] Using fallback rule-based agents")
        
        logging.info("Demo completed successfully")
        return True
        
    except Exception as e:
        logging.error(f"Demo processing error: {e}")
        print(f"\n[ERROR] Error during processing: {e}")
        return False

if __name__ == "__main__":
    test_simple_use_case()