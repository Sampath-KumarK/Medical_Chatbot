import streamlit as st

from utils.embedding import embedding_model
from utils.retriever import retrieve_chunks
from utils.llm import generate_answer

st.set_page_config(
    page_title="Medical Chatbot",
    page_icon="🩺"
)

st.title("🩺 Medical RAG Chatbot")

st.write("Ask medical questions based on the uploaded medical PDF.")

question = st.text_input("Enter your question")

if st.button("Ask"):

    if question.strip() == "":

        st.warning("Please enter a question.")

    else:

        with st.spinner("Searching medical document..."):

            chunks = retrieve_chunks(
                question,
                embedding_model
            )

            context = "\n\n".join(chunks)

            answer = generate_answer(
                question,
                context
            )

        st.subheader("Answer")

        st.write(answer)

        with st.expander("Retrieved Context"):

            st.write(context)

st.divider()

st.info(
    "Educational purposes only. Not medical advice."
)