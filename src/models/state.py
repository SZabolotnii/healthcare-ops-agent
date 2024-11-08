# src/models/state.py
from typing import Annotated, List, Dict, Optional
from typing_extensions import TypedDict  # Changed this import
from langchain_core.messages import AnyMessage
from datetime import datetime
import operator
from enum import Enum
from langchain_core.messages import HumanMessage, SystemMessage, AnyMessage


class TaskType(str, Enum):
    PATIENT_FLOW = "patient_flow"
    RESOURCE_MANAGEMENT = "resource_management"
    QUALITY_MONITORING = "quality_monitoring"
    STAFF_SCHEDULING = "staff_scheduling"
    GENERAL = "general"

class PriorityLevel(int, Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4
    CRITICAL = 5

class Department(TypedDict):
    """Department information"""
    id: str
    name: str
    capacity: int
    current_occupancy: int
    staff_count: Dict[str, int]
    wait_time: int

class PatientFlowMetrics(TypedDict):
    """Metrics related to patient flow"""
    total_beds: int
    occupied_beds: int
    waiting_patients: int
    average_wait_time: float
    admission_rate: float
    discharge_rate: float
    department_metrics: Dict[str, "Department"]

class ResourceMetrics(TypedDict):
    """Metrics related to resource management"""
    equipment_availability: Dict[str, bool]
    supply_levels: Dict[str, float]
    resource_utilization: float
    pending_requests: int
    critical_supplies: List[str]

class QualityMetrics(TypedDict):
    """Metrics related to quality monitoring"""
    patient_satisfaction: float
    care_outcomes: Dict[str, float]
    compliance_rate: float
    incident_count: int
    quality_scores: Dict[str, float]
    last_audit_date: datetime

class StaffingMetrics(TypedDict):
    """Metrics related to staff scheduling"""
    total_staff: int
    available_staff: Dict[str, int]
    shifts_coverage: Dict[str, float]
    overtime_hours: float
    skill_mix_index: float
    staff_satisfaction: float

class HospitalMetrics(TypedDict):
    """Combined hospital metrics"""
    patient_flow: PatientFlowMetrics
    resources: ResourceMetrics
    quality: QualityMetrics
    staffing: StaffingMetrics
    last_updated: datetime

class AnalysisResult(TypedDict):
    """Analysis results from nodes"""
    category: TaskType
    priority: PriorityLevel
    findings: List[str]
    recommendations: List[str]
    action_items: List[Dict[str, str]]
    metrics_impact: Dict[str, float]


class HospitalState(TypedDict):
    """Main state management for the agent"""
    messages: Annotated[List[AnyMessage], operator.add]
    current_task: TaskType
    priority_level: PriorityLevel
    department: Optional[str]
    metrics: HospitalMetrics
    analysis: Optional[AnalysisResult]
    context: Dict[str, any]  # Will include routing information
    timestamp: datetime
    thread_id: str


def create_initial_state(thread_id: str) -> HospitalState:
    """Create initial state with default values"""
    return {       
        "messages": [],
        "current_task": TaskType.GENERAL,
        "priority_level": PriorityLevel.MEDIUM,
        "department": None,
        "metrics": {
            "patient_flow": {
                "total_beds": 300,
                "occupied_beds": 240,
                "waiting_patients": 15,
                "average_wait_time": 35.0,
                "admission_rate": 4.2,
                "discharge_rate": 3.8,
                "department_metrics": {}
            },
            "resources": {
                "equipment_availability": {},
                "supply_levels": {},
                "resource_utilization": 0.75,
                "pending_requests": 5,
                "critical_supplies": []
            },
            "quality": {
                "patient_satisfaction": 8.5,
                "care_outcomes": {},
                "compliance_rate": 0.95,
                "incident_count": 2,
                "quality_scores": {},
                "last_audit_date": datetime.now()
            },
            "staffing": {
                "total_staff": 500,
                "available_staff": {
                    "doctors": 50,
                    "nurses": 150,
                    "specialists": 30,
                    "support": 70
                },
                "shifts_coverage": {},
                "overtime_hours": 120.5,
                "skill_mix_index": 0.85,
                "staff_satisfaction": 7.8
            },
            "last_updated": datetime.now()
        },
        "analysis": None,
        "context": {
             "next_node": None  # Add routing context
        },
        "timestamp": datetime.now(),
        "thread_id": thread_id
    }

def validate_state(state: HospitalState) -> bool:
    """Validate state structure and data types"""
    try:
        # Basic structure validation
        required_keys = [
            "messages", "current_task", "priority_level",
            "metrics", "timestamp", "thread_id"
        ]
        for key in required_keys:
            if key not in state:
                raise ValueError(f"Missing required key: {key}")

        # Validate messages
        if not isinstance(state["messages"], list):
            raise ValueError("Messages must be a list")
        
        # Validate each message has required attributes
        for msg in state["messages"]:
            if not hasattr(msg, 'content'):
                raise ValueError("Invalid message format - missing content")

        # Validate types
        if not isinstance(state["current_task"], TaskType):
            raise ValueError("Invalid task type")
        if not isinstance(state["priority_level"], PriorityLevel):
            raise ValueError("Invalid priority level")
        if not isinstance(state["timestamp"], datetime):
            raise ValueError("Invalid timestamp")

        return True

    except Exception as e:
        raise ValueError(f"State validation failed: {str(e)}")

def update_state_metrics(
    state: HospitalState,
    new_metrics: Dict,
    category: str
) -> HospitalState:
    """Update specific category of metrics in state"""
    if category not in state["metrics"]:
        raise ValueError(f"Invalid metrics category: {category}")
    
    state["metrics"][category].update(new_metrics)
    state["metrics"]["last_updated"] = datetime.now()
    
    return state