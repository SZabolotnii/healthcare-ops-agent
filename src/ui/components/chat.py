import streamlit as st
from typing import Optional, Dict, Callable
from datetime import datetime

class ChatComponent:
    def __init__(self, process_message_callback: Callable):
        """
        Initialize the chat component
        
        Args:
            process_message_callback: Callback function to process messages
        """
        self.process_message = process_message_callback
        
        # Initialize session state for messages if not exists
        if 'messages' not in st.session_state:
            st.session_state.messages = []
            
    def _display_message(self, role: str, content: str, timestamp: Optional[datetime] = None):
        """Display a single chat message"""
        avatar = "🤖" if role == "assistant" else "👤"
        with st.chat_message(role, avatar=avatar):
            st.markdown(content)
            if timestamp:
                st.caption(f":clock2: {timestamp.strftime('%H:%M')}")

    def render(self):
        """Render the chat interface"""
        st.markdown("### 💬 Healthcare Operations Chat")
        
        # Display chat messages
        for message in st.session_state.messages:
            self._display_message(
                role=message["role"],
                content=message["content"],
                timestamp=message.get("timestamp")
            )
        
        # Chat input
        if prompt := st.chat_input(
            "Ask about patient flow, resources, quality metrics, or staff scheduling..."
        ):
            # Add user message
            current_time = datetime.now()
            st.session_state.messages.append({
                "role": "user",
                "content": prompt,
                "timestamp": current_time
            })
            
            # Display user message
            self._display_message("user", prompt, current_time)
            
            # Process message and get response
            with st.spinner("Processing your request... 🔄"):
                try:
                    response = self.process_message(prompt)
                    
                    # Add and display assistant response
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response["response"],
                        "timestamp": datetime.now()
                    })
                    
                    self._display_message(
                        "assistant",
                        response["response"],
                        datetime.now()
                    )
                    
                except Exception as e:
                    st.error(f"Error processing your request: {str(e)} ❌")

    def clear_chat(self):
        """Clear the chat history"""
        st.session_state.messages = []
        st.success("Chat history cleared! 🧹")