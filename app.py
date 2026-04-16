"""DeepTutor - AI-powered tutoring application.

Main entry point for the Streamlit-based web application.
"""

import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="DeepTutor",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed",  # I prefer more reading space by default
)


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = None
    if "document_processed" not in st.session_state:
        st.session_state.document_processed = False
    if "current_mode" not in st.session_state:
        # Default to chat mode - jumping straight into Q&A works better for me
        st.session_state.current_mode = "chat"


def render_sidebar():
    """Render the sidebar with configuration options."""
    with st.sidebar:
        st.title("📚 DeepTutor")
        st.markdown("---")

        # Mode selection
        st.subheader("Mode")
        mode = st.radio(
            "Select interaction mode:",
            options=["chat", "quiz", "summary"],
            format_func=lambda x: {
                "chat": "💬 Chat with Document",
                "quiz": "🧠 Quiz Mode",
                "summary": "📋 Summarize",
            }[x],
        )
        st.session_state.current_mode = mode

        st.markdown("---")

        # Document upload
        st.subheader("Upload Document")
        uploaded_file = st.file_uploader(
            "Upload a PDF to get started",
            # Also accepting .txt files since I often have plain text notes I want to query
            # Added .md support too - I keep a lot of markdown notes
            type=["pdf", "txt", "md"],
            help="Upload a PDF, plain text, or Markdown document to analyze and learn from.",
        )

        if uploaded_file is not None:
            st.session_state.uploaded_file = uploaded_file
            st.success(f"✅ Loaded: {uploaded_file.name}")

        st.markdown("---")
        st.caption("DeepTutor — Powered by LightRAG")


def render_chat_interface():
    """Render the main chat interface."""
    st.title("💬 Chat with Your Document")

    if st.session_state.uploaded_file is None:
        st.info("👈 Upload a PDF document from the sidebar to get started.")
        return

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question about your document..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response (placeholder until pipeline is integrated)
        with st.chat_message("assistant"):
