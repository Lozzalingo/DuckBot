import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer

# Load sentence embedding model
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Connect to database
conn = sqlite3.connect("duckbot.db")
cursor = conn.cursor()

# Fetch all questions
cursor.execute("SELECT question FROM duckboy_info")
questions = cursor.fetchall()

# Compute and store embeddings
for question in questions:
    question_text = question[0]
    embedding = embedding_model.encode([question_text])[0]
    embedding_blob = np.array(embedding, dtype=np.float32).tobytes()

    cursor.execute("UPDATE duckboy_info SET embedding = ? WHERE question = ?", (embedding_blob, question_text))

conn.commit()
conn.close()
