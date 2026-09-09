import streamlit as st

from utils.pdf_loader import load_pdf
from utils.chunker import split_text
from utils.embedding import create_embeddings

st.title("🧠 Embedding Test")

if st.button("Generate Embeddings"):

    pdf_text = load_pdf("data/medical.pdf")

    chunks = split_text(pdf_text)

    embeddings = create_embeddings(chunks)

    st.success(f"Chunks: {len(chunks)}")

    st.success(f"Embeddings: {len(embeddings)}")

    st.write("Shape of one embedding:")

    st.write(len(embeddings[0]))

    st.subheader("First Chunk")

    st.write(chunks[0])

    st.subheader("First 20 Numbers of its Embedding")

    st.write(embeddings[0][:20])