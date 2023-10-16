import os
from dotenv import load_dotenv
import streamlit as st
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import openai

from agents.base_agent import BaseAgent
from memory.memory import Memory
from knowledge_base.knowledge_base import KnowledgeBase
from utils.agent_prompts import base_agent_prompt

def initiate_page():

    # initiate the session
    st.session_state["initiated"] = True

    # initialize the API
    load_dotenv(os.path.join('..', '.env'))
    openai.api_key = os.environ['OPENAI_API_KEY']

    # load vector database
    embeddings = OpenAIEmbeddings()
    st.session_state["vdb"] = FAISS.load_local(os.path.join('vector_databases', 'my_database'), embeddings)

    # initialize agent
    memory = Memory(initial_prompt=base_agent_prompt)
    knowledge_base = KnowledgeBase(st.session_state["vdb"])
    st.session_state['agent'] = BaseAgent(memory=memory, knowledge_base=knowledge_base, model='gpt-3.5-turbo')

def reset_conversation():

    # restart agent
    memory = Memory(initial_prompt=base_agent_prompt)
    knowledge_base = KnowledgeBase(st.session_state["vdb"])
    st.session_state['agent'] = BaseAgent(memory=memory, knowledge_base=knowledge_base, model='gpt-3.5-turbo')

    st.experimental_rerun()