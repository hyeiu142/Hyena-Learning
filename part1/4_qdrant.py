import os
import uuid
from dotenv import load_dotenv
from openai import OpenAI
from langchain_text_splitters import MarkdownTextSplitter
from qdrant_client import QdrantClient 
from qdrant_client.models import Distance, VectorParams, PointStruct

load_dotenv()
client=OpenAI()

with open("result.md", "r", encoding="utf-8") as f:
    text_content = f.read()

splitter = MarkdownTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.create_documents([text_content])

qdrant = QdrantClient("localhost", port=6333)

COLLECTION_NAME = "rag_learning"

if qdrant.collection_exists(COLLECTION_NAME):
    qdrant.delete_collection(COLLECTION_NAME)

qdrant.create_collection(
    collection_name=COLLECTION_NAME, 
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
)

print(f"Collection '{COLLECTION_NAME}' created successfully. Waiting to get vector from OpenAI...")

points = []
for idx, doc in enumerate(chunks):
    res=client.embeddings.create(input=doc.page_content, model="text-embedding-3-small")
    vector=res.data[0].embedding

    points.append(PointStruct(
        id=str(uuid.uuid4()),
        vector=vector, 
        payload={
            "content":doc.page_content,
            "company":"FPT",
            "nam": 2025, 
            "nguon": f"Chunk {idx}"
        }
    ))

qdrant.upsert(
    collection_name=COLLECTION_NAME, 
    points=points
)
print(f"Uploaded {len(points)} vectors to Qdrant")