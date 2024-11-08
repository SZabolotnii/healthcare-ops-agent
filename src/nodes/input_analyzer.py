# src/nodes/input_analyzer.py
#from typing import Dict
from typing import Dict, List, Optional, Any
from typing_extensions import TypedDict  # If using TypedDict
#from langchain_core.messages import SystemMessage, HumanMessage
from ..models.state import HospitalState, TaskType, PriorityLevel
from ..config.prompts import PROMPTS
from ..utils.logger import setup_logger
from langchain_core.messages import HumanMessage, SystemMessage, AnyMessage

logger = setup_logger(__name__)

class InputAnalyzerNode:
    def __init__(self, llm):
        self.llm = llm
        self.system_prompt = PROMPTS["input_analyzer"]

    def __call__(self, state: HospitalState) -> Dict:
        try:
            # Get the latest message
            if not state["messages"]:
                raise ValueError("No messages in state")
                
            latest_message = state["messages"][-1]
            
            # Ensure message is a LangChain message object
            if not hasattr(latest_message, 'content'):
                raise ValueError("Invalid message format")
            
            # Prepare messages for LLM
            messages = [
                SystemMessage(content=self.system_prompt),
                latest_message if isinstance(latest_message, HumanMessage) 
                else HumanMessage(content=str(latest_message))
            ]
            
            # Get LLM response
            response = self.llm.invoke(messages)
            
            # Parse response to determine task type and priority
            parsed_result = self._parse_llm_response(response.content)
            
            return {
                "current_task": parsed_result["task_type"],
                "priority_level": parsed_result["priority"],
                "department": parsed_result["department"],
                "context": parsed_result["context"]
            }
            
        except Exception as e:
            logger.error(f"Error in input analysis: {str(e)}")
            raise

    def _parse_llm_response(self, response: str) -> Dict:
        """Parse LLM response to extract task type and other metadata"""
        try:
            # Default values
            result = {
                "task_type": TaskType.GENERAL,
                "priority": PriorityLevel.MEDIUM,
                "department": None,
                "context": {}
            }
            
            # Simple parsing logic (can be made more robust)
            if "patient flow" in response.lower():
                result["task_type"] = TaskType.PATIENT_FLOW
            elif "resource" in response.lower():
                result["task_type"] = TaskType.RESOURCE_MANAGEMENT
            elif "quality" in response.lower():
                result["task_type"] = TaskType.QUALITY_MONITORING
            elif "staff" in response.lower() or "schedule" in response.lower():
                result["task_type"] = TaskType.STAFF_SCHEDULING
            
            # Extract priority from response
            if "urgent" in response.lower() or "critical" in response.lower():
                result["priority"] = PriorityLevel.CRITICAL
            elif "high" in response.lower():
                result["priority"] = PriorityLevel.HIGH
            
            return result
            
        except Exception as e:
            logger.error(f"Error parsing LLM response: {str(e)}")
            return result
