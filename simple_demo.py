#!/usr/bin/env python3
"""
Simple Demo of AI Agent Sandbox with OpenAI Integration
Demonstrates the system working with GPT-4 powered agents.
"""

from orchestrator import Orchestrator
from config import Config
from openai_utils import check_openai_status
import json


def test_simple_use_case():
    """Test a simple birthday party planning request"""
    
    print("🎉 AI Agent Sandbox - Simple Demo")
    print("=" * 50)
    
    # Check OpenAI status
    print("🔧 Checking OpenAI Configuration...")
    openai_status = check_openai_status()
    
    print(f"✅ API Key: {'Set' if openai_status['api_key_set'] else 'Not Set'}")
    print(f"✅ Model: {openai_status['model']}")
    print(f"✅ Client: {'Configured' if openai_status['configured'] else 'Not Configured'}")
    
    if not openai_status['configured']:
        print("❌ OpenAI not properly configured!")
        return False
    
    # Test connection
    print("\n🧪 Testing OpenAI Connection...")
    if openai_status['connection_test']:
        print("✅ OpenAI connection successful!")
    else:
        print("❌ OpenAI connection failed!")
        return False
    
    # Initialize orchestrator
    print("\n🤖 Initializing AI Agents...")
    orchestrator = Orchestrator()
    
    # Test request
    user_request = "I want to plan a birthday party for my 8-year-old daughter. We'll have about 12 kids."
    
    print(f"\n📝 User Request: {user_request}")
    print("\n⏳ Processing through AI agents...")
    
    try:
        # Process the request
        result = orchestrator.process_user_request(user_request)
        
        # Display results
        print("\n" + "="*60)
        print("🎯 ALBERT CORE (AI-Powered)")
        print("="*60)
        albert_response = result['albert_output']['response']
        print(f"Response: {albert_response}")
        
        print("\n" + "="*60)
        print("📋 PLANNING AGENT (AI-Powered)")
        print("="*60)
        tasks = result['planning_output']['tasks']
        print(f"Generated {len(tasks)} tasks:")
        for i, task in enumerate(tasks, 1):
            print(f"\n{i}. {task['description']}")
            print(f"   Priority: {task['priority']}")
            print(f"   Category: {task.get('details', {}).get('category', 'N/A')}")
            print(f"   Time: {task.get('details', {}).get('estimated_time', 'N/A')}")
            ai_generated = task.get('details', {}).get('ai_generated', False)
            print(f"   AI Generated: {'✅' if ai_generated else '❌'}")
        
        print("\n" + "="*60)
        print("❓ QUESTIONING AGENT (AI-Powered)")
        print("="*60)
        questions = result['questioning_output']['questions']
        missing_details = result['questioning_output']['missing_details']
        
        print(f"Clarifying Questions ({len(questions)}):")
        for i, question in enumerate(questions[:5], 1):  # Show first 5
            print(f"{i}. {question}")
        
        print(f"\nMissing Details Identified ({len(missing_details)}):")
        for i, detail in enumerate(missing_details[:3], 1):  # Show first 3
            print(f"{i}. {detail}")
        
        # Check if AI was used
        refined_plan = result['questioning_output']['refined_plan']
        ai_analysis = refined_plan.get('ai_analysis', False)
        completeness_score = refined_plan.get('completeness_score', 0)
        
        print(f"\nAI Analysis Used: {'✅' if ai_analysis else '❌'}")
        print(f"Plan Completeness Score: {completeness_score:.2f}/1.0")
        
        print("\n" + "="*60)
        print("🎉 FINAL RESULT")
        print("="*60)
        final_result = result['final_result']
        print(f"Summary: {final_result['summary']}")
        
        print(f"\nRecommendations ({len(final_result['recommendations'])}):")
        for i, rec in enumerate(final_result['recommendations'][:3], 1):
            print(f"{i}. {rec}")
        
        print("\n✅ Demo completed successfully!")
        print("🤖 All agents are working with OpenAI GPT-4!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during processing: {e}")
        print("\n🔄 Falling back to simple agents...")
        
        # Try with AI disabled
        Config.ENABLE_AI_AGENTS = False
        result = orchestrator.process_user_request(user_request)
        print("✅ Simple fallback agents working!")
        return False


def main():
    """Main demo function"""
    try:
        success = test_simple_use_case()
        
        if success:
            print("\n🎊 Congratulations! Your AI Agent Sandbox is working perfectly!")
            print("💡 Try running: python main.py for the full interactive demo")
        else:
            print("\n⚠️  AI agents had issues, but fallback agents are working.")
            print("💡 Check your OpenAI API key and internet connection.")
            
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")


if __name__ == "__main__":
    main() 