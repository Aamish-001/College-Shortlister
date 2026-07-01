import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from src.rag import process_documents
from src.chatbot import get_answer

st.header(":green[**SalaryBot**]", divider="violet")

# Initialize Session States so memory persists across page reruns
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- SIDEBAR: Upload & Heavy Processing ---
with st.sidebar:
    st.title("Documents Upload")
    files = st.file_uploader("Upload your documents here", type=["pdf", "docx", "txt", "xlsx"], accept_multiple_files=True)
    
    # The Magic Button: Heavy processing ONLY happens when this is clicked
    process_button = st.button("Process Documents")

if files and process_button:
    with st.spinner("Processing large documents... This might take a minute."):
        st.session_state.vector_store = process_documents(files)
        st.success("Documents successfully indexed! You can chat now.")

# --- MAIN SCREEN: Fast Chat Interface ---
if st.session_state.vector_store is not None:
    
    # Display running chat history
    for role, message in st.session_state.chat_history:
        with st.chat_message(role):
            st.write(message)

    # User input
    user_question = st.chat_input("Ask a question:")

    if user_question:
        # Show user message instantly
        with st.chat_message("user"):
            st.write(user_question)
        st.session_state.chat_history.append(("user", user_question))

        # Setup conversation context for multi-turn search
        history_text = ""
        for role, message in st.session_state.chat_history[:-1]:
            label = "User" if role == "user" else "Assistant"
            history_text += f"{label}: {message}\n"

        past_user_messages = [m for role, m in st.session_state.chat_history[:-1] if role == "user"]
        search_query = past_user_messages[-1] + " " + user_question if past_user_messages else user_question

        question_with_history = f"Previous conversation:\n{history_text}\nCurrent question: {user_question}"
        
        # Get response using functions from src/chatbot.py
        response = get_answer(st.session_state.vector_store, search_query, question_with_history)

        # Show AI answer
        with st.chat_message("assistant"):
            st.write(response)
        st.session_state.chat_history.append(("assistant", response))
else:
    st.info("Please upload your company terms documents in the sidebar and click 'Process Documents' to begin.")