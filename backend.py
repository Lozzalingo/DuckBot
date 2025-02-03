import sys
import sqlite3
import subprocess
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

# Function to call Ollama with dynamic prompt
def call_ollama(user_input):
    try:
        model_name = "llama3.2:latest"  # Replace with your AI model

        # Try fetching relevant fact from database
        retrieved_fact = search_duckboy_facts(user_input)

        if retrieved_fact:
            final_prompt = f"The user asked this: {user_input}. Here's some addional information: {retrieved_fact}. When you reply, get into character and respond as Duck Boy.\n\n. Keep the response short but funny."
        else:
            final_prompt = f"Remember, you are Duck Boy and you should respond in character.\n\n{user_input}. Keep the response short but funny."

        # Call Ollama with final prompt
        result = subprocess.run(
            ["ollama", "run", model_name],
            input=final_prompt,
            text=True,
            capture_output=True
        )
        response = result.stdout.strip()
        return response
    except Exception as e:
        print(f"Error generating reply: {e}")
        return "Oops, I seem to have short-circuited!"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
        print(call_ollama(user_input))
    else:
        print("No input provided.")
