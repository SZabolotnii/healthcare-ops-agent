# examples/usage_examples.py
import os
from dotenv import load_dotenv
from src.agent import HealthcareAgent

# Load environment variables
load_dotenv()

def basic_usage_example():
    """Basic usage example of the Healthcare Agent"""
    agent = HealthcareAgent(os.getenv("OPENAI_API_KEY"))
    
    # Single query example
    response = agent.process(
        "What is the current ER wait time and bed availability?"
    )
    print("Basic Query Response:", response)

def conversation_example():
    """Example of maintaining conversation context"""
    agent = HealthcareAgent()
    thread_id = "example-conversation"
    
    # Series of related queries
    queries = [
        "How many beds are currently available in the ER?",
        "What is the current staffing level for that department?",
        "Based on these metrics, what are your recommendations for optimization?"
    ]
    
    for query in queries:
        print(f"\nUser: {query}")
        response = agent.process(query, thread_id=thread_id)
        print(f"Assistant: {response['response']}")

def department_analysis_example():
    """Example of department-specific analysis"""
    agent = HealthcareAgent()
    
    # Context with department-specific metrics
    context = {
        "department": "ICU",
        "metrics": {
            "bed_capacity": 20,
            "occupied_beds": 18,
            "staff_count": {"doctors": 5, "nurses": 15},
            "average_stay": 4.5  # days
        }
    }
    
    response = agent.process(
        "Analyze current ICU operations and suggest improvements",
        context=context
    )
    print("Department Analysis:", response)

def async_streaming_example():
    """Example of using async streaming responses"""
    import asyncio
    
    async def stream_response():
        agent = HealthcareAgent()
        query = "Provide a complete analysis of current hospital operations"
        
        async for event in agent.graph.astream_events(
            {"messages": [query]},
            {"configurable": {"thread_id": "streaming-example"}}
        ):
            if event["event"] == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                if content:
                    print(content, end="", flush=True)
    
    asyncio.run(stream_response())

if __name__ == "__main__":
    print("=== Basic Usage Example ===")
    basic_usage_example()
    
    print("\n=== Conversation Example ===")
    conversation_example()
    
    print("\n=== Department Analysis Example ===")
    department_analysis_example()
    
    print("\n=== Streaming Example ===")
    async_streaming_example()# Usage examples implementation
