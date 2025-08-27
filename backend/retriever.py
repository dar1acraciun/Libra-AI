from pathlib import Path
import os
import openai
from dotenv import load_dotenv
import chromadb
from chromadb.config import Settings

DATA_FILE=Path("data") / "books.json"
PERSIST_DIR = "./.chroma"            
COLLECTION = "book_summaries"

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
def search(query):

    emb = openai.embeddings.create(model="text-embedding-3-small", input=[query])
    query_vector = emb.data[0].embedding

    client = chromadb.PersistentClient(
        path=PERSIST_DIR,
        settings=Settings(anonymized_telemetry=False)
    )

    coll=client.get_or_create_collection(COLLECTION)

    results = coll.query(query_embeddings=[query_vector],n_results=3)
    return results


# if __name__ == "__main__":
#     query = input("Introdu tema sau contextul pentru căutare semantică: ")
#     results = search(query)
#     if results and results.get("documents") and results["documents"][0]:
#         for i, doc in enumerate(results["documents"][0]):
#             print(f"Rezultat {i+1}:\n{doc}\n")
#     else:
#         print("Niciun rezultat găsit.")



