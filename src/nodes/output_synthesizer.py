# src/nodes/output_synthesizer.py
#from typing import Dict, List
from typing import Dict, List, Optional, Any
from typing_extensions import TypedDict  # If using TypedDict
from langchain_core.messages import SystemMessage
from ..models.state import HospitalState
from ..config.prompts import PROMPTS
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class OutputSynthesizerNode:
    def __init__(self, llm):
        self.llm = llm
        self.system_prompt = PROMPTS["output_synthesis"]

    def __call__(self, state: HospitalState) -> Dict:
        try:
            # Get analysis results from previous nodes
            analysis = state.get("analysis", {})
            
            # Format prompt with context
            formatted_prompt = self.system_prompt.format(
                context=self._format_context(state)
            )
            
            # Get LLM synthesis
            response = self.llm.invoke([
                SystemMessage(content=formatted_prompt)
            ])
            
            # Structure the final output
            final_output = self._structure_final_output(
                response.content,
                state["current_task"],
                state["priority_level"]
            )
            
            return {
                "messages": [response],
                "analysis": final_output
            }
            
        except Exception as e:
            logger.error(f"Error in output synthesis: {str(e)}")
            raise

    def _format_context(self, state: HospitalState) -> str:
        """Format all relevant context for synthesis"""
        return f"""
Task Type: {state['current_task']}
Priority Level: {state['priority_level']}
Department: {state['department'] or 'All Departments'}
Key Metrics Summary:
- Patient Flow: {self._summarize_patient_flow(state)}
- Resources: {self._summarize_resources(state)}
- Quality: {self._summarize_quality(state)}
- Staffing: {self._summarize_staffing(state)}
        """

    def _structure_final_output(self, response: str, task_type: str, priority: int) -> Dict:
        """Structure the final output in a standardized format"""
        return {
            "summary": self._extract_summary(response),
            "key_findings": self._extract_key_findings(response),
            "recommendations": self._extract_recommendations(response),
            "action_items": self._extract_action_items(response),
            "priority_level": priority,
            "task_type": task_type
        }

    def _summarize_patient_flow(self, state: HospitalState) -> str:
        metrics = state["metrics"]["patient_flow"]
        return f"Occupancy {(metrics['occupied_beds']/metrics['total_beds'])*100:.1f}%"

    def _summarize_resources(self, state: HospitalState) -> str:
        metrics = state["metrics"]["resources"]
        return f"Utilization {metrics['resource_utilization']*100:.1f}%"

    def _summarize_quality(self, state: HospitalState) -> str:
        metrics = state["metrics"]["quality"]
        return f"Satisfaction {metrics['patient_satisfaction']:.1f}/10"

    def _summarize_staffing(self, state: HospitalState) -> str:
        metrics = state["metrics"]["staffing"]
        return f"Staff Available: {sum(metrics['available_staff'].values())}"

    def _extract_summary(self, response: str) -> str:
        """Extract high-level summary from response"""
        # Implementation depends on response structure
        return response.split('\n')[0]

    def _extract_key_findings(self, response: str) -> List[str]:
        """Extract key findings from response"""
        findings = []
        # Implementation for parsing findings
        return findings

    def _extract_recommendations(self, response: str) -> List[str]:
        """Extract recommendations from response"""
        recommendations = []
        # Implementation for parsing recommendations
        return recommendations

    def _extract_action_items(self, response: str) -> List[Dict]:
        """Extract actionable items from response"""
        action_items = []
        # Implementation for parsing action items
        return action_items# output_synthesizer node implementation
