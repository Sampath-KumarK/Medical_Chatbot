import streamlit as st
from utils.pdf_loader import load_pdf

st.title("📄 PDF Reader Test")

if st.button("Read PDF"):

    pdf_text = load_pdf("data/medical.pdf")

    st.success("PDF Loaded Successfully!")

    st.text_area(
        "Extracted Text",
        pdf_text,
        height=400
    )