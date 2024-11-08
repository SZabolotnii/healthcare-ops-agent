# tests/conftest.py
import pytest
from datetime import datetime
from typing import Dict

from src.config.settings import Settings
from src.models.state import HospitalState, TaskType, PriorityLevel

@pytest.fixture
def mock_settings():
    """Fixture for test settings"""
    return {
        "OPENAI_API_KEY": "test-api-key",
        "MODEL_NAME": "gpt-4o-mini-2024-07-18",
        "MODEL_TEMPERATURE": 0,
        "MEMORY_TYPE": "sqlite",
        "MEMORY_URI": ":memory:",
        "LOG_LEVEL": "DEBUG"
    }

@pytest.fixture
def mock_llm_response():
    """Fixture for mock LLM responses"""
    return {
        "input_analysis": {
            "task_type": TaskType.PATIENT_FLOW,
            "priority": PriorityLevel.HIGH,
            "department": "ER",
            "context": {"urgent": True}
        },
        "patient_flow": {
            "recommendations": ["Optimize bed allocation", "Increase staff in ER"],
            "metrics": {"waiting_time": 25, "bed_utilization": 0.85}
        },
        "quality_monitoring": {
            "satisfaction_score": 8.5,
            "compliance_rate": 0.95,
            "recommendations": ["Maintain current standards"]
        }
    }

@pytest.fixture
def mock_hospital_state() -> HospitalState:
    """Fixture for mock hospital state"""
    return {
        "messages": [],
        "current_task": TaskType.GENERAL,
        "priority_level": PriorityLevel.MEDIUM,
        "department": None,
        "metrics": {
            "patient_flow": {
                "total_beds": 100,
                "occupied_beds": 75,
                "waiting_patients": 10,
                "average_wait_time": 30.0
            },
            "resources": {
                "equipment_availability": {"ventilators": True},
                "supply_levels": {"masks": 0.8},
                "resource_utilization": 0.75
            },
            "quality": {
                "patient_satisfaction": 8.5,
                "compliance_rate": 0.95,
                "incident_count": 2
            },
            "staffing": {
                "total_staff": 200,
                "available_staff": {"doctors": 20, "nurses": 50},
                "overtime_hours": 45.5
            }
        },
        "analysis": None,
        "context": {},
        "timestamp": datetime.now(),
        "thread_id": "test-thread-id"
    }

@pytest.fixture
def mock_tools_response():
    """Fixture for mock tool responses"""
    return {
        "patient_tools": {
            "wait_time": 30.5,
            "bed_capacity": {"available": 25, "total": 100},
            "discharge_time": datetime.now()
        },
        "resource_tools": {
            "supply_levels": {"critical": [], "reorder": ["masks"]},
            "equipment_status": {"available": ["xray"], "in_use": ["mri"]}
        }
    }

@pytest.fixture
def mock_error_response():
    """Fixture for mock error responses"""
    return {
        "validation_error": {
            "code": "INVALID_INPUT",
            "message": "Invalid input parameters",
            "details": {"field": "department", "issue": "required"}
        },
        "processing_error": {
            "code": "PROCESSING_FAILED",
            "message": "Failed to process request",
            "details": {"step": "analysis", "reason": "timeout"}
        }
    }# Test configuration implementation
