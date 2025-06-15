import streamlit as st
from graph import *
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import tempfile

st.title("Aman HR Recruiter Chatbot")

def get_pdf_content():
    if "docs" in st.session_state:
        return st.session_state.docs
    else:
        return None

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

with st.sidebar:
    uploaded_files = st.file_uploader("Upload your resumes (PDF)", type=["pdf"], accept_multiple_files=True)
    if uploaded_files:
        all_contents = []
        for uploaded_file in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_path = tmp_file.name

            # Load resume using LangChain
            loader = PyPDFLoader(tmp_path)
            pages = loader.load()
            all_contents.append(pages[0].page_content)

        # Combine all PDF contents with a separator
        st.session_state.docs = "\n\n---\n\n".join(all_contents)

# Handle user input
if prompt := st.chat_input("What's on your mind today?"):
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({"role":"user", "content": prompt})

    # Convert history to LangGraph-compatible format
    langgraph_messages = [(m["role"], m["content"]) for m in st.session_state.messages]

    # Prepare state with pdf_content if available
    state = {"messages": langgraph_messages}
    if "docs" in st.session_state and st.session_state.docs:
        state["pdf_content"] = st.session_state.docs

    # Stream the response from the graph
    response_text = ""
    config = {"configurable":{"thread_id":"single_session_memory"}}
    for event in graph.stream(state, config):
        for value in event.values():
            for msg in value["messages"]:
                if msg.type == "ai":
                    response_text += msg.content

    # Display AI message
    with st.chat_message("ai"):
        st.markdown(response_text)

    # Append AI response to session history
    st.session_state.messages.append({"role": "ai", "content": response_text})


