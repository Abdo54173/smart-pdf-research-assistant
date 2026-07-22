import streamlit as st

from api_client import ask_question, upload_pdf
from components import render_sources


st.set_page_config(
    page_title="Smart PDF Assistant",
    page_icon="📄",
)

st.title("📄 Smart PDF Research Assistant")

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"],
)

if uploaded_file:

    if st.button("Upload"):

        with st.spinner("Uploading document..."):

            response = upload_pdf(uploaded_file)

            st.session_state.conversation_id = response["conversation_id"]

            st.success(response["message"])

question = st.chat_input("Ask a question...")

if question:

    with st.spinner("Thinking..."):

        response = ask_question(
            st.session_state.conversation_id,
            question,
        )

        st.chat_message("user").write(question)

        st.chat_message("assistant").write(
            response["answer"]
        )

        render_sources(response["sources"])