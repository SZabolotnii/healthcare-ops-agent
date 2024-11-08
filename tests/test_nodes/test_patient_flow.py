# tests/test_nodes/test_patient_flow.py
import pytest
from src.nodes.patient_flow import PatientFlowNode

def test_patient_flow_analysis(mock_hospital_state, mock_llm_response):
    """Test patient flow analysis"""
    node = PatientFlowNode(mock_llm_response)
    result = node(mock_hospital_state)
    
    assert "analysis" in result
    assert "messages" in result
    assert "recommendations" in result["analysis"]

def test_occupancy_calculation(mock_hospital_state):
    """Test occupancy calculation logic"""
    node = PatientFlowNode(None)
    metrics = mock_hospital_state["metrics"]["patient_flow"]
    
    occupancy = node._calculate_occupancy(metrics)
    expected = (metrics["occupied_beds"] / metrics["total_beds"]) * 100
    
    assert occupancy == expected