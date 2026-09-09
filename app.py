import streamlit as st
import ollama

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Medical Chatbot",
    page_icon="🩺",
    layout="centered"
)

st.title("🩺 Medical Chatbot using LLM")
st.write("Ask medical-related questions.")

# -------------------------------
# User Input
# -------------------------------
question = st.text_input("Enter your medical question:")

# -------------------------------
# Medical Keywords
# -------------------------------
medical_keywords = [
    "doctor", "medicine", "medical", "health", "disease",
    "symptom", "treatment", "fever", "pain", "infection",
    "virus", "bacteria", "covid", "diabetes", "cancer",
    "heart", "blood", "hospital", "asthma", "malaria",
    "dengue", "tablet", "headache", "vomiting", "cough",
    "cold", "surgery", "patient", "kidney", "liver"
]

# -------------------------------
# Ask Button
# -------------------------------
if st.button("Ask"):

    if question.strip() == "":
        st.warning("Please enter a question.")

    else:

        # Check whether question is medical
        is_medical = any(
            keyword in question.lower()
            for keyword in medical_keywords
        )

        if not is_medical:

            st.error(
                "❌ I am a medical chatbot. Please ask only medical-related questions."
            )

        else:

            with st.spinner("Thinking..."):

                response = ollama.chat(
                    model="llama3.2:3b",
                    messages=[
                        {
                            "role": "system",
                            "content": """
You are a helpful medical assistant.

Rules:

1. Answer only medical questions.

2. Explain answers in simple language.

3. Never claim to be a doctor.

4. If you are unsure, say that the user should consult a healthcare professional.

5. End every answer with:

'This information is for educational purposes only and is not a substitute for professional medical advice.'
"""
                        },
                        {
                            "role": "user",
                            "content": question
                        }
                    ]
                )

                answer = response["message"]["content"]

            st.subheader("🤖 Medical Assistant")

            st.write(answer)

# -------------------------------
# Disclaimer
# -------------------------------
st.divider()

st.info(
    "⚠️ This chatbot provides educational information only. "
    "It should not be used for medical diagnosis or treatment."
)