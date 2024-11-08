# tests/test_nodes/test_input_analyzer.py
import pytest
from src.nodes.input_analyzer import InputAnalyzerNode
from src.models.state import TaskType, PriorityLevel

def test_input_analyzer_initialization(mock_llm_response):
    """Test InputAnalyzer node initialization"""
    analyzer = InputAnalyzerNode(mock_llm_response)
    assert analyzer is not None

def test_input_analysis(mock_hospital_state, mock_llm_response):
    """Test input analysis functionality"""
    analyzer = InputAnalyzerNode(mock_llm_response)
    result = analyzer(mock_hospital_state)
    
    assert "current_task" in result
    assert "priority_level" in result
    assert isinstance(result["current_task"], TaskType)
    assert isinstance(result["priority_level"], PriorityLevel)

def test_invalid_input_handling(mock_hospital_state):
    """Test handling of invalid input"""
    analyzer = InputAnalyzerNode(None)
    mock_hospital_state["messages"] = []
    
    with pytest.raises(ValueError):
        analyzer(mock_hospital_state)