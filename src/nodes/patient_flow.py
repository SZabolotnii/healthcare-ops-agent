# src/nodes/patient_flow.py
#from typing import Dict
from typing import Dict, List, Optional, Any
from typing_extensions import TypedDict  # If using TypedDict
from langchain_core.messages import SystemMessage
from ..models.state import HospitalState
from ..config.prompts import PROMPTS
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class PatientFlowNode:
    def __init__(self, llm):
        self.llm = llm
        self.system_prompt = PROMPTS["patient_flow"]

    def __call__(self, state: HospitalState) -> Dict:
        try:
            # Get current metrics
            metrics = state["metrics"]["patient_flow"]
            
            # Format prompt with current metrics
            formatted_prompt = self.system_prompt.format(
                occupancy=self._calculate_occupancy(metrics),
                wait_times=metrics["average_wait_time"],
                department_capacity=self._get_department_capacity(metrics),
                admission_rate=metrics["admission_rate"]
            )
            
            # Get LLM analysis
            response = self.llm.invoke([
                SystemMessage(content=formatted_prompt)
            ])
            
            # Parse and structure the response
            analysis = self._structure_analysis(response.content)
            
            return {
                "analysis": analysis,
                "messages": [response]
            }
            
        except Exception as e:
            logger.error(f"Error in patient flow analysis: {str(e)}")
            raise

    def _calculate_occupancy(self, metrics: Dict) -> float:
        """Calculate current occupancy percentage"""
        return (metrics["occupied_beds"] / metrics["total_beds"]) * 100

    def _get_department_capacity(self, metrics: Dict) -> Dict:
        """Get capacity details by department"""
        return metrics.get("department_metrics", {})

    def _structure_analysis(self, response: str) -> Dict:
        """Structure the LLM response into a standardized format"""
        return {
            "findings": [],  # Extract key findings
            "recommendations": [],  # Extract recommendations
            "action_items": [],  # Extract action items
            "metrics_impact": {}  # Expected impact on metrics
        }# patient_flow node implementation
