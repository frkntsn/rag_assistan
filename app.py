import streamlit as st

from src.pipeline.rag_pipeline import run_rag
from src.storage.sqlite_store import clear_sqlite_logs, init_sqlite
from src.vectorstore.chroma_store import reset_collection


st.set_page_config(page_title="Local Wiki RAG", page_icon=":books:")
st.title("Local Wikipedia RAG Assistant")
init_sqlite()

with st.sidebar:
    show_context = st.checkbox("Show retrieved context", value=False)
    top_k = st.slider("Top-k", min_value=1, max_value=10, value=5)
    clear_chat = st.button("Clear chat")
    reset_system = st.button("Reset system")

if "messages" not in st.session_state:
    st.session_state.messages = []

if clear_chat:
    st.session_state.messages = []
    st.rerun()

if reset_system:
    reset_collection()
    clear_sqlite_logs()
    st.session_state.messages = []
    st.success("System reset complete. Re-run indexing before asking questions.")

with st.form("ask_form", clear_on_submit=True):
    query = st.text_input("Ask a question about famous people and places:")
    submitted = st.form_submit_button("Ask")

if submitted and query.strip():
    with st.spinner("Thinking..."):
        result = run_rag(query=query, top_k=top_k)
    st.session_state.messages.append(
        {
            "query": query,
            "route": result["route"],
            "answer": result["answer"],
            "context_docs": result["context_docs"],
        }
    )

for item in reversed(st.session_state.messages):
    st.markdown(f"**Question:** {item['query']}")
    st.markdown(f"**Route:** `{item['route']}`")
    st.markdown(f"**Answer:** {item['answer']}")

    if show_context and item["context_docs"]:
        st.subheader("Retrieved context")
        for i, doc in enumerate(item["context_docs"], start=1):
            st.markdown(f"**Chunk {i}**")
            st.write(doc)
