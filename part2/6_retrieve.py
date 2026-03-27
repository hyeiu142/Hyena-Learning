from dotenv import load_dotenv
from openai import OpenAI
from qdrant_client import QdrantClient

load_dotenv()
client = OpenAI()
qdrant = QdrantClient("localhost", port=6333)

COLLECTION_NAME = "rag_learning"

question = "Lợi nhuận tổng của FPT sau thuế năm 2025 là bao nhiêu?"

print(f"Question: {question}")
print("Searching chunk relevant...\n")

res = client.embeddings.create(input=question, model="text-embedding-3-small")
question_vector = res.data[0].embedding

search_result = qdrant.query_points(
    collection_name=COLLECTION_NAME,
    query=question_vector,
    limit=3
).points

for idx, hit in enumerate(search_result):
    # hit.score: cosine similarity score
    # hit.payload: metadata and content
    print(f"Top {idx+1} | Cosine: {hit.score:.4f}---")
    print(f"Source: {hit.payload['nguon']}")
    print(hit.payload['content'][:300] + "...")
    print("\n")
    




