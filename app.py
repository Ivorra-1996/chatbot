import streamlit as st
import ollama
import re


def clean_response(text):
    cleaned = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    cleaned = re.sub(r'\n\s*\n', '\n\n', cleaned)
    return cleaned.strip()

def get_ai_response(message):
    try:
        response = ollama.chat(
            model="deepseek-r1:1.5b",
            messages=[{'role': 'user', 'content': message}],
        )
        return clean_response(response['message']['content'])
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    st.title("Chat con DeepSeek-r1:1.5b")
    st.write("Una aplicacion simple de chat usando Streamlit y DeepSeek-r1:1.5b a través de Ollama. 😌")

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

    if prompt := st.chat_input("Escribe tu mensaje..."):
        st.session_state.messages.append({'role': 'user', 'content': prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        response = get_ai_response(prompt)
        st.session_state.messages.append({'role': 'assistant', 'content': response})
        with st.chat_message("assistant"):
            st.markdown(response)

if __name__ == "__main__":
    main()
