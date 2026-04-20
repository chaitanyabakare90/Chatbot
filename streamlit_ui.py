import streamlit as st
from chat_backend import generate_response  # ✅ fixed typo

st.title("FinAssist")

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

    # ✅ Build chat history in the format backend expects: {"user": ..., "assistant": ...}
    formatted_history = []
    messages = st.session_state.messages
    for i in range(0, len(messages) - 1, 2):
        if messages[i]["role"] == "user" and messages[i + 1]["role"] == "assistant":
            formatted_history.append({
                "user": messages[i]["content"],
                "assistant": messages[i + 1]["content"]
            })

    # ✅ Pass last 3 pairs to backend
    chat_history = formatted_history[-3:]

    # ✅ Add user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})

    # ✅ Generate response
    response = generate_response(query=prompt, chat_history=chat_history)

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)

    # Add assistant response to session state
    st.session_state.messages.append({"role": "assistant", "content": response})
