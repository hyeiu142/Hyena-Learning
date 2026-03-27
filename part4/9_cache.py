import numpy as np 
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    return dot_product / (norm1 * norm2)

semantic_cache = []

# User A ask (nothing in Cache)
print("User A ask once")
q1 = "Lợi nhuận sau thuế của FPT năm 2025 là bao nhiêu?"
print(f"User A: {q1}")

v1 = client.embeddings.create(input=q1, model="text-embedding-3-small").data[0].embedding
answer1 = "FPT đạt 11.226 tỷ đồng lãi sau thuế năm 2025."

print(f"Answer user A: {answer1}")

semantic_cache.append({
    "q_vector":v1, 
    "answer":answer1
})

print(f"Save cache to Semantic Cache\n")

# User B ask similar question
print("User B ask similar question")
q2 = "Năm 2025 FPT đã kiếm được bao nhiêu tiền lãi sau thuế?"
print(f"User B: {q2}")

v2 = client.embeddings.create(input=q1, model = "text-embedding-3-small").data[0].embedding

cache_hit = False
for item in semantic_cache: 
    score = cosine_similarity(v2, item["q_vector"])
    print(f"Comparison with cache... Score: {score:.4f}")
    if score > 0.9:
        print(f"Cache Hit! Using cached answer")
        cache_hit = True
        break
if not cache_hit: 
    print("Cache Miss! Generating new answer...")
    
        