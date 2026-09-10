import ollama


def generate_answer(question, context):

    prompt = f"""
You are a helpful medical assistant.

Answer ONLY using the information provided in the context.

If the answer is not available in the context, say:

"I couldn't find this information in the provided medical document."

Context:
{context}

Question:
{question}

Answer:
"""

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]