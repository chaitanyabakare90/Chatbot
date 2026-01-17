import streamlit as st
from chat_backend import generate_respone
st.title("Agro_Share")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("How can I help you?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    history_chat= st.session_state.messages[-3:]
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    response = generate_respone(query=prompt, chat_history=history_chat)
    response_str= f"Edu: {response}"
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})