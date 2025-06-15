import os
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
from langgraph.graph import MessagesState
from langchain_core.messages import SystemMessage
from app import get_pdf_content


# Define our model
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_Groq = ChatGroq(api_key=GROQ_API_KEY, model="meta-llama/llama-4-scout-17b-16e-instruct", temperature=0)

# Shared State
class SharedState(MessagesState):
    pass

# Nodes
def agent(state: SharedState):
    system_msg = open("SYSTEM_MSG.txt","r").read()
    pdf_content = get_pdf_content()
    job_requirements = open("D:\\LangChain\\Self Trial\\project_test1\\job_requirements_data.txt","r").read()
    # job_requirements = open("D:\\LangChain\\Self Trial\\project_test1\\job_requirements_mobile.txt","r").read()

    system_msg = system_msg.format(resume_content=pdf_content, job_requirements=job_requirements)
    
    messages = [SystemMessage(content=system_msg)] + state["messages"]
    response = LLM_Groq.invoke(messages)
    return {"messages": [response]}
