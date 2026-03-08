import json
import os
import numpy as np
from flask import Flask, request, jsonify, render_template
from sklearn.metrics.pairwise import cosine_similarity
from mistralai import Mistral

# ----------------------------------
# Configuration
# ----------------------------------

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY") #add environmental varaible with API KEY before running the code

if not MISTRAL_API_KEY:
    raise ValueError("MISTRAL_API_KEY not found in environment variables")

EMBED_MODEL = "mistral-embed"
CHAT_MODEL = "mistral-small"

client = Mistral(api_key=MISTRAL_API_KEY)

app = Flask(__name__)

# ----------------------------------
# Load documents
# ----------------------------------

with open("docs.json", "r", encoding="utf-8") as f:
    documents = json.load(f)

doc_texts = [doc["content"] for doc in documents]

# ----------------------------------
# Generate embeddings for documents
# ----------------------------------

print("Generating embeddings for documents...")

if os.path.exists("doc_embeddings.npy"):

    print("Loading cached embeddings...")

    doc_embeddings = np.load("doc_embeddings.npy")

else:

    print("Generating embeddings...")

    doc_embeddings = []
    batch_size = 50

    for i in range(0, len(doc_texts), batch_size):

        batch = doc_texts[i:i+batch_size]

        response = client.embeddings.create(
            model=EMBED_MODEL,
            inputs=batch
        )

        for item in response.data:
            doc_embeddings.append(item.embedding)

    doc_embeddings = np.array(doc_embeddings)

    np.save("doc_embeddings.npy", doc_embeddings)

    print("Embeddings saved.")


# ----------------------------------
# Conversation history storage
# ----------------------------------

sessions = {}

# ----------------------------------
# Similarity search (consine similarity is used instead of vector DB )
# ----------------------------------

def retrieve_chunks(query, top_k=3):

    query_embed = client.embeddings.create(
        model=EMBED_MODEL,
        inputs=[query]
    ).data[0].embedding

    similarities = cosine_similarity(
        [query_embed],
        doc_embeddings
    )[0]

    top_indices = similarities.argsort()[-top_k:][::-1]

    retrieved = []

    for idx in top_indices:
        retrieved.append(doc_texts[idx])

    max_similarity = similarities[top_indices[0]]

    return retrieved, max_similarity

# ----------------------------------
# Prompt construction
# ----------------------------------

def build_prompt(context_chunks, history, user_message):

    context = "\n".join(context_chunks)

    history_text = ""

    for h in history:
        history_text += f"User: {h['user']}\nAssistant: {h['assistant']}\n"

    prompt = f"""
You are a nutrition assistant.

Answer the user's question ONLY using the provided context.

If the answer is not present in the context, say:
"I do not have enough information to answer that."

Context:
{context}

Conversation History:
{history_text}

User Question:
{user_message}
"""

    return prompt

# ----------------------------------
# LLM call
# ----------------------------------

def get_llm_response(prompt):

    response = client.chat.complete(
        model=CHAT_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    reply = response.choices[0].message.content

    return reply

# ----------------------------------
# API Endpoint
# ----------------------------------

@app.route("/api/chat", methods=["POST"])
def chat():

    data = request.json

    session_id = data.get("sessionId")
    message = data.get("message")

    if not session_id or not message:
        return jsonify({"error": "Invalid request"}), 400

    if session_id not in sessions:
        sessions[session_id] = []

    history = sessions[session_id][-5:]

    retrieved_chunks, similarity = retrieve_chunks(message)

    if similarity < 0.25:
        return jsonify({
            "reply": "I do not have enough information to answer that.",
            "tokensUsed": 0,
            "retrievedChunks": 0
        })

    prompt = build_prompt(retrieved_chunks, history, message)

    reply = get_llm_response(prompt)

    sessions[session_id].append({
        "user": message,
        "assistant": reply
    })

    return jsonify({
        "reply": reply,
        "retrievedChunks": len(retrieved_chunks)
    })

# ----------------------------------
# Frontend
# ----------------------------------

@app.route("/")
def index():
    return render_template("index.html")

# ----------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)