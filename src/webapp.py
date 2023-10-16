import streamlit as st
from streamlit_chat import message

from flow_control.initialize_and_reset import initiate_page, reset_conversation


# Initiate config of the page
if "initiated" not in st.session_state:
    initiate_page()

# MAIN PAGE

st.title("Malaga42 LLM")

# container for chat history
response_container = st.container()
# container for text box
container = st.container()

with container:
    with st.form(key='my_form', clear_on_submit=True):
        question = st.text_area("You:", key='input', height=100)
        submit_button = st.form_submit_button(label='Ask')

    if submit_button and question:
        with st.spinner('Thinking...'):
            answer = st.session_state["agent"].reply(question)

if st.session_state['agent'].conversation:
    with response_container:
        for i, exchange in enumerate(st.session_state['agent'].conversation):
            human_message, agent_message = exchange
            message(human_message, is_user=True, key=f'human_{i}')
            message(agent_message, allow_html=True, key=f'agent_{i}')

# SIDE BAR

counter_placeholder = st.sidebar.empty()
counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['agent'].total_cost:.5f}")

clear_button = st.sidebar.button("Clear All", key="clear")
if clear_button:
    reset_conversation()
    counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['agent'].total_cost:.5f}")