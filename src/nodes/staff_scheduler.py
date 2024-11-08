# src/nodes/staff_scheduler.py
from typing import Dict, List, Optional, Any
from typing_extensions import TypedDict  # If using TypedDict
from langchain_core.messages import SystemMessage
from ..models.state import HospitalState
from ..config.prompts import PROMPTS
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class StaffSchedulerNode:
    def __init__(self, llm):
        self.llm = llm
        self.system_prompt = PROMPTS["staff_scheduler"]

    def __call__(self, state: HospitalState) -> Dict:
        try:
            # Get current staffing metrics
            metrics = state["metrics"]["staffing"]
            
            # Format prompt with current metrics
            formatted_prompt = self.system_prompt.format(
                staff_available=self._format_staff_availability(metrics),
                department_needs=self._get_department_needs(state),
                skill_requirements=self._format_skill_requirements(metrics),
                work_hours=metrics["overtime_hours"]
            )
            
            # Get LLM analysis
            response = self.llm.invoke([
                SystemMessage(content=formatted_prompt)
            ])
            
            # Generate scheduling recommendations
            analysis = self._generate_schedule_recommendations(response.content, metrics)
            
            return {
                "analysis": analysis,
                "messages": [response],
                "context": {
                    "staff_satisfaction": metrics["staff_satisfaction"],
                    "skill_mix_index": metrics["skill_mix_index"]
                }
            }
            
        except Exception as e:
            logger.error(f"Error in staff scheduling analysis: {str(e)}")
            raise

    def _format_staff_availability(self, metrics: Dict) -> str:
        """Format staff availability into readable text"""
        return ", ".join([
            f"{role}: {count} available"
            for role, count in metrics["available_staff"].items()
        ])

    def _get_department_needs(self, state: HospitalState) -> Dict:
        """Get staffing needs by department"""
        return {
            dept: metrics
            for dept, metrics in state["metrics"]["patient_flow"]["department_metrics"].items()
        }

    def _format_skill_requirements(self, metrics: Dict) -> str:
        """Format skill requirements into readable text"""
        return f"Skill Mix Index: {metrics['skill_mix_index']:.2f}"

    def _generate_schedule_recommendations(self, response: str, metrics: Dict) -> Dict:
        """Generate scheduling recommendations based on LLM response"""
        return {
            "shift_adjustments": [],
            "staff_assignments": {},
            "overtime_recommendations": [],
            "training_needs": [],
            "efficiency_improvements": []
        }# staff_scheduler node implementation
