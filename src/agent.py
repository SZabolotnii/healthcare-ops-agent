# src/agent.py
from typing import Dict, Optional, List
import uuid
from datetime import datetime
from langchain_core.messages import HumanMessage, SystemMessage, AnyMessage
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

# Remove this line as it's causing the error
# from langgraph.checkpoint import BaseCheckpointSaver

from .config.settings import Settings
from .models.state import (
    HospitalState,
    create_initial_state,
    validate_state
)
from .nodes import (
    InputAnalyzerNode,
    TaskRouterNode,
    PatientFlowNode,
    ResourceManagerNode,
    QualityMonitorNode,
    StaffSchedulerNode,
    OutputSynthesizerNode
)
from .tools import (
    PatientTools,
    ResourceTools,
    QualityTools,
    SchedulingTools
)

from .utils.logger import setup_logger
from .utils.error_handlers import (
    ErrorHandler, 
    HealthcareError, 
    ValidationError,  # Add this import
    ProcessingError   # Add this import
)


logger = setup_logger(__name__)

class HealthcareAgent:
    def __init__(self, api_key: Optional[str] = None):
        try:
            # Initialize settings and validate
            self.settings = Settings()
            if api_key:
                self.settings.OPENAI_API_KEY = api_key
            self.settings.validate_settings()
            
            # Initialize LLM
            self.llm = ChatOpenAI(
                model=self.settings.MODEL_NAME,
                temperature=self.settings.MODEL_TEMPERATURE,
                api_key=self.settings.OPENAI_API_KEY
            )
            
            # Initialize tools
            self.tools = self._initialize_tools()
            
            # Initialize nodes
            self.nodes = self._initialize_nodes()
            
            # Initialize conversation states (replacing checkpointer)
            self.conversation_states = {}
            
            # Build graph
            self.graph = self._build_graph()
            
            logger.info("Healthcare Agent initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing Healthcare Agent: {str(e)}")
            raise HealthcareError(
                message="Failed to initialize Healthcare Agent",
                error_code="INIT_ERROR",
                details={"error": str(e)}
            )

    def _initialize_tools(self) -> Dict:
        """Initialize all tools used by the agent"""
        return {
            "patient": PatientTools(),
            "resource": ResourceTools(),
            "quality": QualityTools(),
            "scheduling": SchedulingTools()
        }

    def _initialize_nodes(self) -> Dict:
        """Initialize all nodes in the agent workflow"""
        return {
            "input_analyzer": InputAnalyzerNode(self.llm),
            "task_router": TaskRouterNode(),
            "patient_flow": PatientFlowNode(self.llm),
            "resource_manager": ResourceManagerNode(self.llm),
            "quality_monitor": QualityMonitorNode(self.llm),
            "staff_scheduler": StaffSchedulerNode(self.llm),
            "output_synthesizer": OutputSynthesizerNode(self.llm)
        }

    def _build_graph(self) -> StateGraph:
        """Build the workflow graph with all nodes and edges"""
        try:
            # Initialize graph
            builder = StateGraph(HospitalState)
            
            # Add all nodes
            for name, node in self.nodes.items():
                builder.add_node(name, node)
            
            # Set entry point
            builder.set_entry_point("input_analyzer")
            
            # Add edge from input analyzer to task router
            builder.add_edge("input_analyzer", "task_router")
            
            # Define conditional routing based on task router output
            def route_next(state: Dict):
                return state["context"]["next_node"]
            
            # Add conditional edges from task router
            builder.add_conditional_edges(
                "task_router",
                route_next,
                {
                    "patient_flow": "patient_flow",
                    "resource_management": "resource_manager",
                    "quality_monitoring": "quality_monitor",
                    "staff_scheduling": "staff_scheduler",
                    "output_synthesis": "output_synthesizer"
                }
            )
            
            # Add edges from functional nodes to output synthesizer
            functional_nodes = [
                "patient_flow",
                "resource_manager",
                "quality_monitor",
                "staff_scheduler"
            ]
            
            for node in functional_nodes:
                builder.add_edge(node, "output_synthesizer")
            
            # Add end condition
            builder.add_edge("output_synthesizer", END)
            
            # Compile graph
            return builder.compile()
            
        except Exception as e:
            logger.error(f"Error building graph: {str(e)}")
            raise HealthcareError(
                message="Failed to build agent workflow graph",
                error_code="GRAPH_BUILD_ERROR",
                details={"error": str(e)}
            )

    @ErrorHandler.error_decorator
    def process(
        self,
        input_text: str,
        thread_id: Optional[str] = None,
        context: Optional[Dict] = None
    ) -> Dict:
        """Process input through the healthcare operations workflow"""
        try:
            # Validate input
            ErrorHandler.validate_input(input_text)
            
            # Create or use thread ID
            thread_id = thread_id or str(uuid.uuid4())
            
            # Initialize state
            initial_state = create_initial_state(thread_id)
            
            # Add input message as HumanMessage object
            initial_state["messages"].append(
                HumanMessage(content=input_text)
            )
            
            # Add context if provided
            if context:
                initial_state["context"].update(context)
            
            # Validate state
            validate_state(initial_state)
            
            # Store state in conversation states
            self.conversation_states[thread_id] = initial_state
            
            # Process through graph
            result = self.graph.invoke(initial_state)
            
            return self._format_response(result)
            
        except ValidationError as ve:
            logger.error(f"Validation error: {str(ve)}")
            raise
        except Exception as e:
            logger.error(f"Error processing input: {str(e)}")
            raise HealthcareError(
                message="Failed to process input",
                error_code="PROCESSING_ERROR",
                details={"error": str(e)}
            )

    def _format_response(self, result: Dict) -> Dict:
        """Format the final response from the graph execution"""
        try:
            if not result or "messages" not in result:
                raise ProcessingError(
                    message="Invalid result format",
                    error_code="INVALID_RESULT",
                    details={"result": str(result)}
                )
                
            return {
                "response": result["messages"][-1].content if result["messages"] else "",
                "analysis": result.get("analysis", {}),
                "metrics": result.get("metrics", {}),
                "timestamp": datetime.now()
            }
        except Exception as e:
            logger.error(f"Error formatting response: {str(e)}")
            raise HealthcareError(
                message="Failed to format response",
                error_code="FORMAT_ERROR",
                details={"error": str(e)}
            )

    def get_conversation_history(
        self,
        thread_id: str
    ) -> List[Dict]:
        """Retrieve conversation history for a specific thread"""
        try:
            return self.conversation_states.get(thread_id, {}).get("messages", [])
        except Exception as e:
            logger.error(f"Error retrieving conversation history: {str(e)}")
            raise HealthcareError(
                message="Failed to retrieve conversation history",
                error_code="HISTORY_ERROR",
                details={"error": str(e)}
            )

    def reset_conversation(
        self,
        thread_id: str
    ) -> bool:
        """Reset conversation state for a specific thread"""
        try:
            self.conversation_states[thread_id] = create_initial_state(thread_id)
            return True
        except Exception as e:
            logger.error(f"Error resetting conversation: {str(e)}")
            raise HealthcareError(
                message="Failed to reset conversation",
                error_code="RESET_ERROR",
                details={"error": str(e)}
            )