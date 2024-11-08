# tests/test_tools/test_patient_tools.py
import pytest
from src.tools.patient_tools import PatientTools

def test_wait_time_calculation():
    """Test wait time calculation"""
    tools = PatientTools()
    wait_time = tools.calculate_wait_time("ER", 10, 2)
    
    assert isinstance(wait_time, float)
    assert wait_time > 0

def test_bed_capacity_analysis():
    """Test bed capacity analysis"""
    tools = PatientTools()
    result = tools.analyze_bed_capacity(100, 75, 5)
    
    assert "utilization_rate" in result
    assert "status" in result
    assert result["utilization_rate"] == 75.0

def test_invalid_capacity_input():
    """Test handling of invalid capacity input"""
    tools = PatientTools()
    
    with pytest.raises(ValueError):
        tools.analyze_bed_capacity(0, 10, 5)