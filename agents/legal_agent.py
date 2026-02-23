import google.generativeai as genai
from config import GEMINI_API_KEY, MODEL_NAME, DISCLAIMER

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Create model instance
model = genai.GenerativeModel(MODEL_NAME)


def generate_answer(context, question, chat_history):
    # Build conversation history text
    history_text = ""
    for msg in chat_history:
        role = msg["role"]
        content = msg["content"]
        history_text += f"{role.upper()}: {content}\n"

    if context:
        prompt = f"""
You are a professional legal AI assistant.

Here is the conversation so far:
{history_text}

Answer the current legal question using the provided legal context.

Context:
{context}

Current Question:
{question}
"""
    else:
        prompt = f"""
You are a professional legal AI assistant.

Here is the conversation so far:
{history_text}

Answer the current legal question clearly and professionally.
Do not say you lack memory.
Do not mention previous conversation limitations.
Just continue naturally.

Current Question:
{question}
"""

    response = model.generate_content(prompt)

    return response.text + "\n\n" + DISCLAIMER