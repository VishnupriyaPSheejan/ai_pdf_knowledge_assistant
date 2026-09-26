import os
import requests
import streamlit as st

st.set_page_config(page_title="AI PDF Knowledge Assistant", page_icon="📚", layout="wide")

API_URL = st.sidebar.text_input("API URL", os.getenv("API_URL", "http://localhost:8000")).rstrip("/")

st.title("📚 AI PDF Knowledge Assistant")
st.caption("Upload your own PDFs and chat with them using retrieval-augmented generation.")

if "history" not in st.session_state:
    st.session_state.history = []

with st.sidebar:
    st.header("Knowledge Base")
    files = st.file_uploader("Upload PDF documents", type=["pdf"], accept_multiple_files=True)
    if st.button("Index documents", type="primary", disabled=not files):
        payload = [("files", (f.name, f.getvalue(), "application/pdf")) for f in files]
        with st.spinner("Extracting, chunking and indexing documents..."):
            try:
                r = requests.post(f"{API_URL}/documents/index", files=payload, timeout=300)
                r.raise_for_status()
                st.success(f"Indexed: {r.json()}")
            except Exception as exc:
                st.error(f"Indexing failed: {exc}")

    if st.button("Clear conversation"):
        st.session_state.history = []
        st.rerun()

for message in st.session_state.history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask a question about your PDFs...")
if question:
    with st.chat_message("user"):
        st.markdown(question)
    st.session_state.history.append({"role": "user", "content": question})

    with st.chat_message("assistant"):
        with st.spinner("Searching documents and generating an answer..."):
            try:
                r = requests.post(
                    f"{API_URL}/chat",
                    json={"question": question, "history": st.session_state.history},
                    timeout=180,
                )
                r.raise_for_status()
                data = r.json()
                st.markdown(data["answer"])
                if data.get("sources"):
                    with st.expander("Retrieved sources"):
                        for source in data["sources"]:
                            st.write(f"• {source['source']} — page {source['page']} — score {source['score']}")
                st.session_state.history.append({"role": "assistant", "content": data["answer"]})
            except Exception as exc:
                st.error(f"Chat failed: {exc}")
                st.session_state.history.pop()
