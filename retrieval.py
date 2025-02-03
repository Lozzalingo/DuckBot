import sqlite3
import re
import numpy as np
from sentence_transformers import SentenceTransformer

# Load sentence embedding model
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def preprocess_input(user_input):
    # Replace "you" and "your" with "Duck Boy" dynamically
    user_input = re.sub(r'\b[Yy]ou\b', "Duck Boy", user_input)
    user_input = re.sub(r'\b[Yy]our\b', "Duck Boy's", user_input)
    return user_input

def search_duckboy_facts(user_input, k=1):
    conn = sqlite3.connect("duckbot.db")
    cursor = conn.cursor()

    # Apply the text replacement before searching
    user_input = preprocess_input(user_input)

    # Fetch all stored facts along with their embeddings
    cursor.execute("SELECT question, answer, embedding FROM duckboy_info")
    facts = cursor.fetchall()

    if not facts:
        return None  # No facts found

    # Extract stored embeddings and answers
    answers = [fact[1] for fact in facts]
    embeddings = [np.frombuffer(fact[2], dtype=np.float32) for fact in facts]

    # Compute user input embedding
    input_embedding = embedding_model.encode([user_input])[0]

    # Compute cosine similarity
    embeddings_matrix = np.vstack(embeddings)
    similarities = np.dot(embeddings_matrix, input_embedding) / (
        np.linalg.norm(embeddings_matrix, axis=1) * np.linalg.norm(input_embedding)
    )

    # Get top-k matches
    top_k_indices = similarities.argsort()[-k:][::-1]

    # If similarity is too low, ignore
    threshold = 0.5  # Adjust as needed
    best_match_idx = top_k_indices[0]
    if similarities[best_match_idx] < threshold:
        return None

    return answers[best_match_idx]  # Return best matching answer