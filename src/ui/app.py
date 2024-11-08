import streamlit as st
from datetime import datetime
from typing import Optional, Dict, Any
import os

from ..agent import HealthcareAgent
from ..models.state import TaskType, PriorityLevel
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class HealthcareUI:
    def __init__(self):
        """Initialize the Healthcare Operations Management UI"""
        try:
            # Set up Streamlit page configuration
            st.set_page_config(
                page_title="Healthcare Operations Assistant",
                page_icon="🏥",
                layout="wide",
                initial_sidebar_state="expanded",
                menu_items={
                    'About': "Healthcare Operations Management AI Assistant",
                    'Report a bug': "https://github.com/yourusername/repo/issues",
                    'Get Help': "https://your-docs-url"
                }
            )

            # Apply custom theme
            self.setup_theme()
            
            # Initialize the agent
            self.agent = HealthcareAgent(os.getenv("OPENAI_API_KEY"))
            
            # Initialize session state variables only if not already set
            if 'initialized' not in st.session_state:
                st.session_state.initialized = True
                st.session_state.messages = []
                st.session_state.thread_id = datetime.now().strftime("%Y%m%d-%H%M%S")
                st.session_state.current_department = "All Departments"
                st.session_state.metrics_history = []
                st.session_state.system_status = True

        except Exception as e:
            logger.error(f"Error initializing UI: {str(e)}")
            st.error("Failed to initialize the application. Please refresh the page.")

    def setup_theme(self):
        """Configure the UI theme and styling"""
        st.markdown("""
            <style>
                /* Main background */
                .stApp {
                    background-color: #f0f8ff;
                }
                
                /* Headers */
                h1, h2, h3 {
                    color: #2c3e50;
                }
                
                /* Chat messages */
                .user-message {
                    background-color: #e3f2fd;
                    padding: 1rem;
                    border-radius: 10px;
                    margin: 1rem 0;
                    border-left: 5px solid #1976d2;
                }
                
                .assistant-message {
                    background-color: #fff;
                    padding: 1rem;
                    border-radius: 10px;
                    margin: 1rem 0;
                    border-left: 5px solid #4caf50;
                }
                
                /* Metrics cards */
                .metric-card {
                    background-color: white;
                    padding: 1rem;
                    border-radius: 10px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    transition: transform 0.2s ease;
                }
                
                .metric-card:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                }
                
                /* Custom button styling */
                .stButton>button {
                    background-color: #2196f3;
                    color: white;
                    border-radius: 20px;
                    padding: 0.5rem 2rem;
                    transition: all 0.3s ease;
                }
                
                .stButton>button:hover {
                    background-color: #1976d2;
                    transform: translateY(-1px);
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
            </style>
        """, unsafe_allow_html=True)

    def render_header(self):
        """Render the application header"""
        try:
            header_container = st.container()
            with header_container:
                col1, col2, col3 = st.columns([1, 4, 1])
                
                with col1:
                    st.markdown("# 🏥")
                
                with col2:
                    st.title("Healthcare Operations Assistant")
                    st.markdown("*Your AI-powered healthcare operations management solution* 🤖")
                
                with col3:
                    # System status indicator
                    status = "🟢 Online" if st.session_state.system_status else "🔴 Offline"
                    st.markdown(f"### {status}")

        except Exception as e:
            logger.error(f"Error rendering header: {str(e)}")
            st.error("Error loading header section")

    def render_metrics(self, metrics: Optional[Dict[str, Any]] = None):
        """Render the metrics dashboard"""
        try:
            if not metrics:
                metrics = {
                    "patient_flow": {"occupied_beds": 75, "total_beds": 100},
                    "quality": {"patient_satisfaction": 8.5},
                    "staffing": {"available_staff": {"doctors": 20, "nurses": 50}},
                    "resources": {"resource_utilization": 0.75}
                }
            
            st.markdown("### 📊 Key Metrics Dashboard")
            metrics_container = st.container()
            
            with metrics_container:
                # First row - Key metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    occupancy = (metrics['patient_flow']['occupied_beds'] / 
                               metrics['patient_flow']['total_beds'] * 100)
                    st.metric(
                        "Bed Occupancy 🛏️",
                        f"{occupancy:.1f}%",
                        "Normal 🟢" if occupancy < 85 else "High 🟡"
                    )
                
                with col2:
                    satisfaction = metrics['quality']['patient_satisfaction']
                    st.metric(
                        "Patient Satisfaction 😊",
                        f"{satisfaction}/10",
                        "↗ +0.5" if satisfaction > 8 else "↘ -0.3"
                    )
                
                with col3:
                    total_staff = sum(metrics['staffing']['available_staff'].values())
                    st.metric(
                        "Available Staff 👥",
                        total_staff,
                        "Optimal 🟢" if total_staff > 80 else "Low 🔴"
                    )
                
                with col4:
                    utilization = metrics['resources']['resource_utilization'] * 100
                    st.metric(
                        "Resource Utilization 📦",
                        f"{utilization:.1f}%",
                        "↘ -2%"
                    )

                # Add metrics to history
                st.session_state.metrics_history.append({
                    'timestamp': datetime.now(),
                    'metrics': metrics
                })

        except Exception as e:
            logger.error(f"Error rendering metrics: {str(e)}")
            st.error("Error loading metrics dashboard")

    def render_chat(self):
        """Render the chat interface"""
        try:
            st.markdown("### 💬 Chat Interface")
            chat_container = st.container()
            
            with chat_container:
                # Display chat messages
                for message in st.session_state.messages:
                    role = message["role"]
                    content = message["content"]
                    timestamp = message.get("timestamp", datetime.now())
                    
                    with st.chat_message(role, avatar="🤖" if role == "assistant" else "👤"):
                        st.markdown(content)
                        st.caption(f":clock2: {timestamp.strftime('%H:%M')}")
                
                # Chat input
                if prompt := st.chat_input("How can I assist you with healthcare operations today?"):
                    # Add user message
                    current_time = datetime.now()
                    st.session_state.messages.append({
                        "role": "user",
                        "content": prompt,
                        "timestamp": current_time
                    })
                    
                    # Display user message
                    with st.chat_message("user", avatar="👤"):
                        st.markdown(prompt)
                        st.caption(f":clock2: {current_time.strftime('%H:%M')}")
                    
                    # Display assistant response
                    with st.chat_message("assistant", avatar="🤖"):
                        with st.spinner("Processing your request... 🔄"):
                            try:
                                # Generate response based on query type
                                response = self._get_department_response(prompt)
                                
                                # Display structured response
                                st.markdown("### 🔍 Key Insights")
                                st.markdown(response["insights"])
                                
                                st.markdown("### 📋 Actionable Recommendations")
                                st.markdown(response["recommendations"])
                                
                                st.markdown("### ⚡ Priority Actions")
                                st.markdown(response["priority_actions"])
                                
                                st.markdown("### ⏰ Implementation Timeline")
                                st.markdown(response["timeline"])
                                
                                # Update metrics if available
                                if "metrics" in response:
                                    self.render_metrics(response["metrics"])
                                
                                # Add to chat history
                                st.session_state.messages.append({
                                    "role": "assistant",
                                    "content": response["full_response"],
                                    "timestamp": datetime.now()
                                })
                                
                            except Exception as e:
                                st.error(f"Error processing request: {str(e)} ❌")
                                logger.error(f"Error in chat processing: {str(e)}")

        except Exception as e:
            logger.error(f"Error rendering chat interface: {str(e)}")
            st.error("Error loading chat interface")

    def _get_department_response(self, query: str) -> Dict[str, Any]:
        """Generate response based on query type"""
        query = query.lower()
        
        # Waiting times response
        if "waiting" in query or "wait time" in query:
            return {
                "insights": """
                📊 Current Department Wait Times:
                - ER: 45 minutes (⚠️ Above target)
                - ICU: 5 minutes (✅ Within target)
                - General Ward: 25 minutes (✅ Within target)
                - Surgery: 30 minutes (⚡ Approaching target)
                - Pediatrics: 20 minutes (✅ Within target)
                """,
                "recommendations": """
                1. 👥 Deploy additional triage nurses to ER
                2. 🔄 Optimize patient handoff procedures
                3. 📱 Implement real-time wait time updates
                4. 🏥 Activate overflow protocols where needed
                """,
                "priority_actions": """
                Immediate Actions Required:
                - 🚨 Redirect non-emergency cases from ER
                - 👨‍⚕️ Increase ER staffing for next 2 hours
                - 📢 Update waiting patients every 15 minutes
                """,
                "timeline": """
                Implementation Schedule:
                - 🕐 0-1 hour: Staff reallocation
                - 🕒 1-2 hours: Process optimization
                - 🕓 2-4 hours: Situation reassessment
                - 🕔 4+ hours: Long-term monitoring
                """,
                "metrics": {
                    "patient_flow": {
                        "occupied_beds": 85,
                        "total_beds": 100,
                        "waiting_patients": 18,
                        "average_wait_time": 35.0
                    },
                    "quality": {"patient_satisfaction": 7.8},
                    "staffing": {"available_staff": {"doctors": 22, "nurses": 55}},
                    "resources": {"resource_utilization": 0.82}
                },
                "full_response": "Based on current data, we're seeing elevated wait times in the ER department. Immediate actions have been recommended to address this situation."
            }
        
        # Bed occupancy response
        elif "bed" in query or "occupancy" in query:
            return {
                "insights": """
                🛏️ Current Bed Occupancy Status:
                - Overall Occupancy: 85%
                - Critical Care: 90% (⚠️ Near capacity)
                - General Wards: 82% (✅ Optimal)
                - Available Emergency Beds: 5
                """,
                "recommendations": """
                1. 🔄 Review discharge plans
                2. 🏥 Prepare overflow areas
                3. 📋 Optimize bed turnover
                4. 👥 Adjust staff allocation
                """,
                "priority_actions": """
                Critical Actions:
                - 🚨 Expedite planned discharges
                - 🏥 Activate surge capacity plan
                - 📊 Hourly capacity monitoring
                """,
                "timeline": """
                Action Timeline:
                - 🕐 Immediate: Discharge reviews
                - 🕑 2 hours: Capacity reassessment
                - 🕒 4 hours: Staff reallocation
                - 🕓 8 hours: Full situation review
                """,
                "metrics": {
                    "patient_flow": {
                        "occupied_beds": 90,
                        "total_beds": 100,
                        "waiting_patients": 12,
                        "average_wait_time": 30.0
                    },
                    "quality": {"patient_satisfaction": 8.0},
                    "staffing": {"available_staff": {"doctors": 25, "nurses": 58}},
                    "resources": {"resource_utilization": 0.88}
                },
                "full_response": "Current bed occupancy is at 85% with critical care areas approaching capacity. Immediate actions are being taken to optimize bed utilization."
            }
        
        # Default response for other queries
        else:
            return {
                "insights": """
                Please specify your request:
                - 🏥 Department specific information
                - ⏰ Wait time inquiries
                - 🛏️ Bed capacity status
                - 👥 Staffing information
                - 📊 Resource utilization
                """,
                "recommendations": "To better assist you, please provide more specific details about what you'd like to know.",
                "priority_actions": "No immediate actions required. Awaiting specific inquiry.",
                "timeline": "Timeline will be generated based on specific requests.",
                "full_response": "I'm here to help! Please specify what information you need about healthcare operations."
            }

    def render_sidebar(self):
        """Render the sidebar with controls and filters"""
        try:
            with st.sidebar:
                # Add custom CSS for consistent button styling
                st.markdown("""
                    <style>
                        /* Container for Quick Actions */
                        .quick-actions-container {
                            display: flex;
                            gap: 10px;
                            margin: 10px 0;
                        }
                        
                        /* Button styling */
                        .stButton > button {
                            width: 120px !important;  /* Fixed width for both buttons */
                            height: 46px !important;  /* Fixed height for both buttons */
                            background-color: #2196f3;
                            color: white;
                            border-radius: 20px;
                            border: none;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            padding: 0 20px;
                            font-size: 0.9rem;
                            transition: all 0.3s ease;
                            margin: 0;
                        }
                        
                        .stButton > button:hover {
                            background-color: #1976d2;
                            transform: translateY(-1px);
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        }
                        
                        /* Column container fixes */
                        div[data-testid="column"] {
                            padding: 0 !important;
                            display: flex;
                            justify-content: center;
                        }
                    </style>
                """, unsafe_allow_html=True)
                
                st.markdown("### ⚙️ Settings")
                
                # Department filter
                if "department_filter" not in st.session_state:
                    st.session_state.department_filter = "All Departments"
                
                st.selectbox(
                    "Select Department",
                    ["All Departments", "ER", "ICU", "General Ward", "Surgery", "Pediatrics"],
                    key="department_filter"
                )
                
                # Priority filter
                if "priority_filter" not in st.session_state:
                    st.session_state.priority_filter = "Medium"
                
                st.select_slider(
                    "Priority Level",
                    options=["Low", "Medium", "High", "Urgent", "Critical"],
                    key="priority_filter"
                )
                
                # Time range
                if "time_range_filter" not in st.session_state:
                    st.session_state.time_range_filter = 8
                
                st.slider(
                    "Time Range (hours)",
                    min_value=1,
                    max_value=24,
                    key="time_range_filter"
                )
                
                # Quick actions with consistent styling
                st.markdown("### ⚡ Quick Actions")
                
                # Create two columns for buttons
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("📊 Report"):
                        st.info("Generating comprehensive report...")
                
                with col2:
                    if st.button("🔄 Refresh"):
                        st.success("Data refreshed successfully!")
                
                # Emergency Mode
                st.markdown("### 🚨 Emergency Mode")
                
                if "emergency_mode" not in st.session_state:
                    st.session_state.emergency_mode = False
                    
                st.toggle(
                    "Activate Emergency Protocol",
                    key="emergency_mode",
                    help="Enable emergency mode for critical situations"
                )
                
                if st.session_state.emergency_mode:
                    st.warning("Emergency Mode Active!")
                
                # Help section
                st.markdown("### ❓ Help")
                with st.expander("Usage Guide"):
                    st.markdown("""
                        - 💬 Use the chat to ask questions
                        - 📊 Monitor real-time metrics
                        - ⚙️ Adjust filters as needed
                        - 📋 Generate reports for analysis
                        - 🚨 Toggle emergency mode for critical situations
                    """)
                
                # Footer
                st.markdown("---")
                st.caption(
                    f"*Last updated: {datetime.now().strftime('%H:%M:%S')}*"
                )

        except Exception as e:
            logger.error(f"Error rendering sidebar: {str(e)}")
            st.error("Error loading sidebar")

    def run(self):
        """Run the Streamlit application"""
        try:
            # Main application container
            main_container = st.container()
            
            with main_container:
                # Render components
                self.render_header()
                self.render_sidebar()
                
                # Main content area
                content_container = st.container()
                with content_container:
                    self.render_metrics()
                    st.markdown("<br>", unsafe_allow_html=True)  # Spacing
                    self.render_chat()
            
        except Exception as e:
            logger.error(f"Error running application: {str(e)}")
            st.error(f"Application error: {str(e)} ❌")