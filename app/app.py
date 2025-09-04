# app/app.py
import streamlit as st
import ollama
import os
import re

MODEL_NAME = os.environ.get("MODEL_NAME", "deepseek-r1:8b")

def clean_response(text):
    cleaned = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    cleaned = re.sub(r'\n\s*\n', '\n\n', cleaned)
    return cleaned.strip()

def get_ai_response(messages):
    try:
        # Mandamos TODO el historial para mantener el contexto
        resp = ollama.chat(model=MODEL_NAME, messages=messages)
        return clean_response(resp["message"]["content"])
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    st.title(f"Chat con {MODEL_NAME}")
    st.write("App simple de chat usando Streamlit y Ollama. 😌")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "Eres un asistente útil y breve."}
        ]

    for m in st.session_state.messages:
        if m["role"] in ("user", "assistant"):
            with st.chat_message(m["role"]):
                st.markdown(m["content"])

    if prompt := st.chat_input("Escribe tu mensaje..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        reply = get_ai_response(st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)

    if st.button("🧹 Reiniciar chat"):
        st.session_state.messages = [
            {"role": "system", "content": "Eres un asistente útil y breve."}
        ]
        st.rerun()

if __name__ == "__main__":
    main()
