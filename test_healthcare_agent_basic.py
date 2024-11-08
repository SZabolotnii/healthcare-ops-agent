# test_healthcare_agent_basic.py
import os
from datetime import datetime
from src.agent import HealthcareAgent
from src.models.state import TaskType, PriorityLevel
from src.utils.error_handlers import ValidationError, HealthcareError

def main():
    """Basic test of the Healthcare Operations Management Agent"""
    try:
        # 1. Test Agent Initialization
        print("\n=== Testing Agent Initialization ===")
        agent = HealthcareAgent(os.getenv("OPENAI_API_KEY"))
        print("✓ Agent initialized successfully")
        
        # 2. Test Basic Query - Patient Flow
        print("\n=== Testing Patient Flow Query ===")
        patient_query = "What is the current ER occupancy and wait time?"
        response = agent.process(
            input_text=patient_query,
            thread_id="test-thread-1"
        )
        print(f"Query: {patient_query}")
        print(f"Response: {response.get('response', 'No response')}")
        print(f"Analysis: {response.get('analysis', {})}")
        
        # 3. Test Resource Management Query
        print("\n=== Testing Resource Management Query ===")
        resource_query = "Check the current availability of ventilators and ICU beds"
        response = agent.process(
            input_text=resource_query,
            thread_id="test-thread-1"
        )
        print(f"Query: {resource_query}")
        print(f"Response: {response.get('response', 'No response')}")
        print(f"Analysis: {response.get('analysis', {})}")
        
        # 4. Test Conversation History
        print("\n=== Testing Conversation History ===")
        history = agent.get_conversation_history("test-thread-1")
        print(f"Conversation history length: {len(history)}")
        
        # 5. Test Reset Conversation
        print("\n=== Testing Conversation Reset ===")
        reset_success = agent.reset_conversation("test-thread-1")
        print(f"Reset successful: {reset_success}")
        
        # 6. Test Error Handling
        print("\n=== Testing Error Handling ===")
        try:
            agent.process("")
            print("❌ Error handling test failed - empty input accepted")
        except ValidationError as ve:
            print(f"✓ Error handling working correctly: Empty input rejected with validation error")
        except HealthcareError as he:
            print(f"✓ Error handling working correctly: {str(he)}")
        except Exception as e:
            print(f"❌ Unexpected error type: {type(e).__name__}: {str(e)}")
            
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")

if __name__ == "__main__":
    print("Starting Healthcare Agent Basic Tests...")
    print(f"Test Time: {datetime.now()}")
    main()