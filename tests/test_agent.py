# tests/test_agent.py
import pytest
from src.agent import HealthcareAgent
from src.utils.error_handlers import HealthcareError

class TestHealthcareAgent:
    def test_agent_initialization(self, mock_settings):
        """Test agent initialization"""
        agent = HealthcareAgent(api_key=mock_settings["OPENAI_API_KEY"])
        assert agent is not None
        assert agent.llm is not None
        assert agent.tools is not None
        assert agent.nodes is not None

    def test_process_input(self, mock_hospital_state):
        """Test processing of input through agent"""
        agent = HealthcareAgent()
        result = agent.process(
            "What is the current ER waiting time?",
            thread_id="test-thread"
        )
        
        assert "response" in result
        assert "analysis" in result
        assert "metrics" in result
        assert "timestamp" in result

    def test_conversation_history(self):
        """Test conversation history retrieval"""
        agent = HealthcareAgent()
        thread_id = "test-thread"
        
        # Add some messages
        agent.process("Test message 1", thread_id=thread_id)
        agent.process("Test message 2", thread_id=thread_id)
        
        history = agent.get_conversation_history(thread_id)
        assert len(history) >= 2

    def test_error_handling(self):
        """Test error handling in agent"""
        agent = HealthcareAgent()
        
        with pytest.raises(HealthcareError):
            agent.process("", thread_id="test-thread")

    def test_state_management(self, mock_hospital_state):
        """Test state management"""
        agent = HealthcareAgent()
        thread_id = "test-thread"
        
        # Process message
        result = agent.process("Test message", thread_id=thread_id)
        assert result is not None
        
        # Reset conversation
        reset_success = agent.reset_conversation(thread_id)
        assert reset_success is True
        
        # Verify reset
        history = agent.get_conversation_history(thread_id)
        assert len(history) == 0

    @pytest.mark.asyncio
    async def test_async_processing(self):
        """Test async processing capabilities"""
        agent = HealthcareAgent()
        thread_id = "test-thread"
        
        # Test streaming response
        async for event in agent.graph.astream_events(
            {"messages": ["Test message"]},
            {"configurable": {"thread_id": thread_id}}
        ):
            assert event is not None# Integration tests implementation
