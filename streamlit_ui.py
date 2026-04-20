import streamlit as st
from chat_backend import generate_respone

st.title("FinAssist 💰")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("How can I help you?"):

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get last 3 exchanges (6 messages) BEFORE appending current message
    history_chat = st.session_state.messages[-6:]

    # Append user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate response
    with st.spinner("Thinking..."):
        response = generate_respone(query=prompt, chat_history=history_chat)

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)

    # Append assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response})
