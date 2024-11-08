import streamlit as st
from typing import Dict, Any, Callable
from datetime import datetime, timedelta

class SidebarComponent:
    def __init__(self, on_filter_change: Optional[Callable] = None):
        """
        Initialize the sidebar component
        
        Args:
            on_filter_change: Optional callback for filter changes
        """
        self.on_filter_change = on_filter_change
        
        # Initialize session state for filters if not exists
        if 'filters' not in st.session_state:
            st.session_state.filters = {
                'department': 'All Departments',
                'priority': 'Medium',
                'time_range': 8,
                'view_mode': 'Standard'
            }

    def render(self):
        """Render the sidebar"""
        with st.sidebar:
            st.markdown("# ⚙️ Operations Control")
            
            # Department Selection
            st.markdown("### 🏥 Department")
            department = st.selectbox(
                "Select Department",
                [
                    "All Departments",
                    "Emergency Room",
                    "ICU",
                    "General Ward",
                    "Surgery",
                    "Pediatrics",
                    "Cardiology"
                ],
                index=0,
                help="Filter data by department"
            )

            # Priority Filter
            st.markdown("### 🎯 Priority Level")
            priority = st.select_slider(
                "Set Priority",
                options=["Low", "Medium", "High", "Urgent", "Critical"],
                value=st.session_state.filters['priority'],
                help="Filter by priority level"
            )

            # Time Range
            st.markdown("### 🕒 Time Range")
            time_range = st.slider(
                "Select Time Range",
                min_value=1,
                max_value=24,
                value=st.session_state.filters['time_range'],
                help="Time range for data analysis (hours)"
            )

            # View Mode
            st.markdown("### 👁️ View Mode")
            view_mode = st.radio(
                "Select View Mode",
                ["Standard", "Detailed", "Compact"],
                help="Change the display density"
            )

            # Quick Actions
            st.markdown("### ⚡ Quick Actions")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📊 Report", use_container_width=True):
                    st.info("Generating report...")
            with col2:
                if st.button("🔄 Refresh", use_container_width=True):
                    st.success("Data refreshed!")

            # Emergency Mode Toggle
            st.markdown("### 🚨 Emergency Mode")
            emergency_mode = st.toggle(
                "Activate Emergency Protocol",
                help="Enable emergency mode for critical situations"
            )
            if emergency_mode:
                st.warning("Emergency Mode Active!")

            # Help & Documentation
            with st.expander("❓ Help & Tips"):
                st.markdown("""
                    ### Quick Guide
                    - 🔍 Use filters to focus on specific areas
                    - 📈 Monitor real-time metrics
                    - 🚨 Toggle emergency mode for critical situations
                    - 📊 Generate reports for analysis
                    - 💡 Access quick actions for common tasks
                """)

            # Update filters in session state
            st.session_state.filters.update({
                'department': department,
                'priority': priority,
                'time_range': time_range,
                'view_mode': view_mode,
                'emergency_mode': emergency_mode
            })

            # Call filter change callback if provided
            if self.on_filter_change:
                self.on_filter_change(st.session_state.filters)

            # Footer
            st.markdown("---")
            st.markdown(
                f"*Last updated: {datetime.now().strftime('%H:%M:%S')}*",
                help="Last data refresh timestamp"
            )