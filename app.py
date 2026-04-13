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
    initial_sidebar_state="expanded",
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
            type=["pdf"],
            help="Upload a PDF document to analyze and learn from.",
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
            with st.spinner("Thinking..."):
                response = f"I received your question: '{prompt}'. The document processing pipeline will be integrated shortly."
                st.markdown(response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )


def render_quiz_interface():
    """Render the quiz mode interface."""
    st.title("🧠 Quiz Mode")
    if st.session_state.uploaded_file is None:
        st.info("👈 Upload a PDF document from the sidebar to generate a quiz.")
        return
    st.info("Quiz generation will be available once the document pipeline is set up.")


def render_summary_interface():
    """Render the document summary interface."""
    st.title("📋 Document Summary")
    if st.session_state.uploaded_file is None:
        st.info("👈 Upload a PDF document from the sidebar to generate a summary.")
        return
    st.info("Document summarization will be available once the pipeline is set up.")


def main():
    """Main application entry point."""
    initialize_session_state()
    render_sidebar()

    mode = st.session_state.current_mode
    if mode == "chat":
        render_chat_interface()
    elif mode == "quiz":
        render_quiz_interface()
    elif mode == "summary":
        render_summary_interface()


if __name__ == "__main__":
    main()
