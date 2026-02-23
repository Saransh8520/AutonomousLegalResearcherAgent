import streamlit as st
from agents.classifier import is_legal_query
from agents.legal_agent import generate_answer
from tools.retriever import initialize_db, retrieve_context

st.set_page_config(page_title="Autonomous Legal AI", page_icon="⚖️")

st.title("⚖️ Autonomous Legal Research Agent")

# Initialize DB
initialize_db()

# Sidebar Clear Chat Button
st.sidebar.header("Session Controls")

if st.sidebar.button("🗑 Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Initialize Session Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
query = st.chat_input("Ask your legal question...")

if query and query.strip() != "":
    # Display user message
    st.chat_message("user").markdown(query)
    st.session_state.messages.append({"role": "user", "content": query})

    if not is_legal_query(query):
        response = (
            "I only answer legal-related questions.\n\n"
            "Disclaimer: This is an AI legal chatbot."
        )
        st.chat_message("assistant").markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

    else:
        context, score = retrieve_context(query)

        if score < 0.5:
            source = "📚 Dataset"
            confidence = "High"
            answer = generate_answer(context, query, st.session_state.messages)
        else:
            source = "🧠 General Legal Knowledge (Gemini)"
            confidence = "Medium"
            answer = generate_answer("", query, st.session_state.messages)

        final_response = f"""
**Source:** {source}  
**Confidence:** {confidence}  

{answer}
"""

        st.chat_message("assistant").markdown(final_response)
        st.session_state.messages.append({"role": "assistant", "content": final_response})