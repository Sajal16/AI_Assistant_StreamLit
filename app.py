import streamlit as st
import ollama

st.set_page_config(page_title="AI Assistant", page_icon="🤖")

if "history" not in st.session_state:
    st.session_state.history = []

st.title("🤖 AI Assistant")

for chat in st.session_state.history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

def chat_with_ai(messages, model="mistral"):
    response = ollama.chat(model=model, messages=messages, stream=True)
    for chunk in response:
        if "message" in chunk:
            yield chunk["message"]["content"]

if prompt := st.chat_input("Type your message..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.history.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for chunk in chat_with_ai(st.session_state.history):
            full_response += chunk
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    st.session_state.history.append({"role": "assistant", "content": full_response})
