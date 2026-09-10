import streamlit as st

from utils.embedding import embedding_model
from utils.retriever import retrieve_chunks

st.title("🩺 Medical Chatbot - Retriever Test")

question = st.text_input("Ask a medical question")

if st.button("Search"):

    chunks = retrieve_chunks(
        question,
        embedding_model
    )

    st.success("Top Matching Chunks")

    for i, chunk in enumerate(chunks):

        st.subheader(f"Chunk {i+1}")

        st.write(chunk)