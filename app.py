import streamlit as st

from src.agent.pipeline import process_document
from src.agent.agent import answer_question
from src.llm.gemini import generate_response
if "chat_history" not in st.session_state:
    st.session_state.chat_history= []
if "current_file" not in st.session_state:
    st.session_state.current_file = None
if "index" not in st.session_state:
    st.session_state.index = None

if "chunks" not in st.session_state:
    st.session_state.chunks = None

st.title("DocMentor AI")

uploaded_file = st.file_uploader("Upload a PDF",type="pdf")

if uploaded_file:

    

    if st.session_state.current_file != uploaded_file.name:

        index, chunks = process_document(uploaded_file)
        st.session_state.current_file = uploaded_file.name
        st.session_state.index = index
        st.session_state.chunks = chunks

    
    st.success("PDF Processed Successfully")

    question = st.text_input("Ask a Question")

    if question:

        answer = answer_question(question,st.session_state.chat_history,st.session_state.index,st.session_state.chunks,generate_response)
        st.session_state.chat_history.append({"question": question,"answer": answer})
        for chat in st.session_state.chat_history:

            st.markdown(f"**You:** {chat['question']}")

            st.markdown(f"**DocMentor:** {chat['answer']}")