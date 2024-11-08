import streamlit as st
from datetime import datetime

class HeaderComponent:
    def __init__(self):
        """Initialize the header component"""
        # Initialize session state for notifications if not exists
        if 'notifications' not in st.session_state:
            st.session_state.notifications = []

    def _add_notification(self, message: str, type: str = "info"):
        """Add a notification to the session state"""
        st.session_state.notifications.append({
            "message": message,
            "type": type,
            "timestamp": datetime.now()
        })

    def render(self):
        """Render the header"""
        # Main header container
        header_container = st.container()
        
        with header_container:
            # Top row with logo and title
            col1, col2, col3 = st.columns([1, 4, 1])
            
            with col1:
                st.markdown("# 🏥")
            
            with col2:
                st.title("Healthcare Operations Assistant")
                st.markdown("""
                    <div style='padding: 0.5rem 0; color: #4a4a4a;'>
                        *AI-Powered Healthcare Management System* 🤖
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                # Status indicator
                status = "🟢 Online" if st.session_state.get('system_status', True) else "🔴 Offline"
                st.markdown(f"### {status}")

            # Notification area
            if st.session_state.notifications:
                with st.expander("📬 Notifications", expanded=True):
                    for notif in st.session_state.notifications[-3:]:  # Show last 3
                        if notif["type"] == "info":
                            st.info(notif["message"])
                        elif notif["type"] == "warning":
                            st.warning(notif["message"])
                        elif notif["type"] == "error":
                            st.error(notif["message"])
                        elif notif["type"] == "success":
                            st.success(notif["message"])

            # System status bar
            status_cols = st.columns(4)
            with status_cols[0]:
                st.markdown("**System Status:** Operational ✅")
            with status_cols[1]:
                st.markdown("**API Status:** Connected 🔗")
            with status_cols[2]:
                st.markdown("**Load:** Normal 📊")
            with status_cols[3]:
                st.markdown(f"**Last Update:** {datetime.now().strftime('%H:%M')} 🕒")

            # Divider
            st.markdown("---")

    def add_notification(self, message: str, type: str = "info"):
        """Public method to add notifications"""
        self._add_notification(message, type)