# src/nodes/task_router.py
from typing import Literal
from typing import Dict, List, Optional, Any
from typing_extensions import TypedDict  # If using TypedDict
from ..models.state import HospitalState, TaskType
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class TaskRouterNode:
    def __call__(self, state: HospitalState) -> Dict:
        """Route to appropriate node based on task type and return state update"""
        try:
            task_type = state["current_task"]
            
            # Create base state update
            state_update = {
                "messages": state.get("messages", []),
                "current_task": task_type,
                "priority_level": state.get("priority_level"),
                "context": state.get("context", {})
            }
            
            # Add routing information to context
            if task_type == TaskType.PATIENT_FLOW:
                state_update["context"]["next_node"] = "patient_flow"
            elif task_type == TaskType.RESOURCE_MANAGEMENT:
                state_update["context"]["next_node"] = "resource_management"
            elif task_type == TaskType.QUALITY_MONITORING:
                state_update["context"]["next_node"] = "quality_monitoring"
            elif task_type == TaskType.STAFF_SCHEDULING:
                state_update["context"]["next_node"] = "staff_scheduling"
            else:
                state_update["context"]["next_node"] = "output_synthesis"
            
            return state_update
                
        except Exception as e:
            logger.error(f"Error in task routing: {str(e)}")
            # Return default routing to output synthesis on error
            return {
                "messages": state.get("messages", []),
                "context": {"next_node": "output_synthesis"},
                "current_task": state.get("current_task")
            }