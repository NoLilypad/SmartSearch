import os
import sqlite3
from dotenv import load_dotenv
from mistralai import Mistral
import numpy as np


# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

API_KEY = os.getenv('API_KEY')
model = "mistral-embed"

# Path to the database
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'pages.db')

client = Mistral(api_key=API_KEY)

# Get all texts from the database
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute('SELECT id, text FROM pages')
rows = c.fetchall()
conn.close()





# Also get titles for display
texts = [row[1][:2000] for row in rows]
titles = [row[0] for row in rows]  # will update this to fetch titles

# Fetch titles from db rows (row = (id, text)), need to fetch title too
# So, update SQL to SELECT id, title, text FROM pages



def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

if not texts:
    print("No texts found in the database.")
    exit(0)


# Get embeddings for all texts in the db, batching by 10
BATCH_SIZE = 10
db_embeddings = []
for i in range(0, len(texts), BATCH_SIZE):
    batch = texts[i:i+BATCH_SIZE]
    response = client.embeddings.create(
        model=model,
        inputs=batch,
    )
    db_embeddings.extend([e.embedding for e in response.data])


# Loop for multiple user queries without recomputing db embeddings
while True:
    user_text = input("Enter a text to compare (or just press Enter to quit): ")
    if not user_text.strip():
        print("Exiting.")
        break
    user_embedding_response = client.embeddings.create(
        model=model,
        inputs=[user_text],
    )
    user_embedding = user_embedding_response.data[0].embedding

    similarities = [cosine_similarity(user_embedding, emb) for emb in db_embeddings]
    top3_idx = np.argsort(similarities)[-3:][::-1]
    print("##### Top 3 most similar texts in the database:\n")
    for idx in top3_idx:
        print(f"(score={similarities[idx]:.4f}) -----> {texts[idx][:200]}")
