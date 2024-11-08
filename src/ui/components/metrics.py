import streamlit as st
from typing import Dict, Any, Optional

class MetricsComponent:
    def __init__(self):
        """Initialize the metrics component"""
        self.default_metrics = {
            "patient_flow": {
                "occupied_beds": 75,
                "total_beds": 100,
                "waiting_time": 15,
                "discharge_rate": 8
            },
            "quality": {
                "patient_satisfaction": 8.5,
                "compliance_rate": 0.95,
                "incident_count": 2
            },
            "staffing": {
                "available_staff": {
                    "doctors": 20,
                    "nurses": 50,
                    "specialists": 15
                },
                "shift_coverage": 0.92
            },
            "resources": {
                "resource_utilization": 0.75,
                "critical_supplies": 3,
                "equipment_availability": 0.88
            }
        }

    def _render_metric_card(
        self,
        title: str,
        value: Any,
        delta: Optional[str] = None,
        help_text: Optional[str] = None
    ):
        """Render a single metric card"""
        st.metric(
            label=title,
            value=value,
            delta=delta,
            help=help_text
        )

    def render(self, metrics: Optional[Dict[str, Any]] = None):
        """
        Render the metrics dashboard
        
        Args:
            metrics: Optional metrics data to display
        """
        metrics = metrics or self.default_metrics
        
        st.markdown("### 📊 Operational Metrics Dashboard")
        
        # Create two rows of metrics
        row1_cols = st.columns(4)
        row2_cols = st.columns(4)
        
        # First row - Key metrics
        with row1_cols[0]:
            occupancy = (metrics["patient_flow"]["occupied_beds"] / 
                        metrics["patient_flow"]["total_beds"] * 100)
            self._render_metric_card(
                "Bed Occupancy 🛏️",
                f"{occupancy:.1f}%",
                "Normal" if occupancy < 85 else "High",
                "Current bed occupancy rate across all departments"
            )

        with row1_cols[1]:
            satisfaction = metrics["quality"]["patient_satisfaction"]
            self._render_metric_card(
                "Patient Satisfaction 😊",
                f"{satisfaction}/10",
                "↗ +0.5" if satisfaction > 8 else "↘ -0.3",
                "Average patient satisfaction score"
            )

        with row1_cols[2]:
            total_staff = sum(metrics["staffing"]["available_staff"].values())
            self._render_metric_card(
                "Available Staff 👥",
                total_staff,
                "Optimal" if total_staff > 80 else "Low",
                "Total number of available staff across all roles"
            )

        with row1_cols[3]:
            utilization = metrics["resources"]["resource_utilization"] * 100
            self._render_metric_card(
                "Resource Utilization 📦",
                f"{utilization:.1f}%",
                "Efficient" if utilization < 80 else "High",
                "Current resource utilization rate"
            )

        # Second row - Additional metrics
        with row2_cols[0]:
            self._render_metric_card(
                "Waiting Time ⏰",
                f"{metrics['patient_flow']['waiting_time']} min",
                help_text="Average patient waiting time"
            )

        with row2_cols[1]:
            self._render_metric_card(
                "Compliance Rate ✅",
                f"{metrics['quality']['compliance_rate']*100:.1f}%",
                help_text="Current compliance rate with protocols"
            )

        with row2_cols[2]:
            self._render_metric_card(
                "Critical Supplies ⚠️",
                metrics['resources']['critical_supplies'],
                "Action needed" if metrics['resources']['critical_supplies'] > 0 else "All stocked",
                "Number of supplies needing immediate attention"
            )

        with row2_cols[3]:
            self._render_metric_card(
                "Shift Coverage 📅",
                f"{metrics['staffing']['shift_coverage']*100:.1f}%",
                help_text="Current shift coverage rate"
            )

        # Additional visualization if needed
        with st.expander("📈 Detailed Metrics Analysis"):
            st.markdown("""
                ### Trend Analysis
                - 📈 Patient flow is within normal range
                - 📉 Resource utilization shows optimization opportunities
                - 📊 Staff distribution is balanced across departments
            """)