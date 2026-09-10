import streamlit as st

from utils.pdf_loader import load_pdf
from utils.chunker import split_text
from utils.embedding import create_embeddings
from utils.chroma_db import store_embeddings

st.title("🩺 Medical Chatbot - Stage 3.4")

if st.button("Store Embeddings"):

    pdf_text = load_pdf("data/medical.pdf")

    chunks = split_text(pdf_text)

    embeddings = create_embeddings(chunks)

    total = store_embeddings(chunks, embeddings)

    st.success(f"✅ Successfully stored {total} chunks in ChromaDB!")