import json, hashlib
from pathlib import Path

import chromadb
from chromadb.config import Settings
import openai
from dotenv import load_dotenv


DATA_FILE=Path("data") / "books.json"
PERSIST_DIR = "./.chroma"            
COLLECTION = "book_summaries"

def make_id(title: str) -> str:
    return hashlib.md5(title.encode("utf-8")).hexdigest()


def main(): 
    import os
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")                 
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))

    client = chromadb.PersistentClient(
        path=PERSIST_DIR,
        settings=Settings(anonymized_telemetry=False)
    )

    coll=client.get_or_create_collection(COLLECTION)
   

    documents, metadatas, ids = [], [], []
    for row in data:
        text = f"Title: {row['title']}\nThemes: {', '.join(row['themes'])}\nSummary: {row['short_summary']}"
        documents.append(text)
        metadatas.append({"title": row["title"], "themes": ", ".join(row["themes"])})
        ids.append(make_id(row["title"]))
    

    emb = openai.embeddings.create(model="text-embedding-3-small", input=documents)
    vectors = [e.embedding for e in emb.data]

    coll.add(documents=documents, metadatas=metadatas, ids=ids, embeddings=vectors)

    print(f"Ingest OK. Elemente în colecție: {len(ids)}")


if __name__ == "__main__":
    main()


