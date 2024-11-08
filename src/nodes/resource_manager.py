# src/nodes/resource_manager.py
from typing import Dict, List, Optional, Any
from typing_extensions import TypedDict  # If using TypedDict
#from typing import Dict
from langchain_core.messages import SystemMessage
from ..models.state import HospitalState
from ..config.prompts import PROMPTS
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class ResourceManagerNode:
    def __init__(self, llm):
        self.llm = llm
        self.system_prompt = PROMPTS["resource_manager"]
        
    def __call__(self, state: HospitalState) -> Dict:
        try:
            # Get current resource metrics
            metrics = state["metrics"]["resources"]
            
            # Format prompt with current metrics
            formatted_prompt = self.system_prompt.format(
                equipment_status=self._format_equipment_status(metrics),
                supply_levels=self._format_supply_levels(metrics),
                resource_allocation=metrics["resource_utilization"],
                budget_info=self._get_budget_info(state)
            )
            
            # Get LLM analysis
            response = self.llm.invoke([
                SystemMessage(content=formatted_prompt)
            ])
            
            # Update state with recommendations
            analysis = self._parse_recommendations(response.content)
            
            return {
                "analysis": analysis,
                "messages": [response],
                "context": {
                    "critical_supplies": metrics["critical_supplies"],
                    "pending_requests": metrics["pending_requests"]
                }
            }
            
        except Exception as e:
            logger.error(f"Error in resource management analysis: {str(e)}")
            raise

    def _format_equipment_status(self, metrics: Dict) -> str:
        """Format equipment availability into readable text"""
        status = []
        for equip, available in metrics["equipment_availability"].items():
            status.append(f"{equip}: {'Available' if available else 'In Use'}")
        return ", ".join(status)

    def _format_supply_levels(self, metrics: Dict) -> str:
        """Format supply levels into readable text"""
        levels = []
        for item, level in metrics["supply_levels"].items():
            status = "Critical" if level < 0.2 else "Low" if level < 0.4 else "Adequate"
            levels.append(f"{item}: {status} ({level*100:.0f}%)")
        return ", ".join(levels)

    def _get_budget_info(self, state: HospitalState) -> str:
        """Get budget information from context"""
        return state.get("context", {}).get("budget_info", "Budget information not available")

    def _parse_recommendations(self, response: str) -> Dict:
        """Parse LLM recommendations into structured format"""
        return {
            "resource_optimization": [],
            "supply_management": [],
            "equipment_maintenance": [],
            "budget_allocation": [],
            "priority_actions": []
        }# resource_manager node implementation
