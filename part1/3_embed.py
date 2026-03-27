import os
from dotenv import load_dotenv
from openai import OpenAI
from langchain_text_splitters import MarkdownTextSplitter

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

with open("result.md", "r", encoding="utf-8") as f:
    text_content = f.read()
splitter = MarkdownTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks=splitter.create_documents([text_content])
embed_chunk= chunks[0].page_content

print(f"Original content: {len(embed_chunk)} characters")

print(embed_chunk[:200] + "...")
print("-" * 50)

print("Sending request to OpenAI to get Vector...")
response = client.embeddings.create(
    input=embed_chunk, 
    model="text-embedding-3-small"
)

vector = response.data[0].embedding
print("-"*50)

print(f"Vector dimension: {len(vector)}")
print(vector[:5])