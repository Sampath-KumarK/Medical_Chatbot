import streamlit as st

from utils.pdf_loader import load_pdf
from utils.chunker import split_text

st.title("📄 PDF Chunking Test")

if st.button("Create Chunks"):

    pdf_text = load_pdf("data/medical.pdf")

    chunks = split_text(pdf_text)

    st.success(f"Total Chunks Created: {len(chunks)}")

    for i, chunk in enumerate(chunks):

        with st.expander(f"Chunk {i+1}"):

            st.write(chunk)