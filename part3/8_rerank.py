from dotenv import load_dotenv
from openai import OpenAI
from qdrant_client import QdrantClient
from sentence_transformers import CrossEncoder
load_dotenv()
client = OpenAI()
qdrant = QdrantClient("localhost", port=6333)
COLLECTION_NAME = "rag_learning"

print("Loading Cross-Encoder model...")
reranker_model = CrossEncoder("BAAI/bge-reranker-v2-m3")

question = "Hoạt động kinh doanh của fpt gồm những lĩnh vực gì?"
print(f"\nUser ask: {question}")

res = client.embeddings.create(input=question, model="text-embedding-3-small")
question_vector = res.data[0].embedding

search_result = qdrant.query_points(
    collection_name=COLLECTION_NAME, 
    query=question_vector,
    limit=20
).points

pairs = []
for hit in search_result:
    pairs.append((question, hit.payload['content']))

scores = reranker_model.predict(pairs)

scored_hits = [{"score": scores[i], "hit": search_result[i]} for i in range(len(search_result))]

scored_hits.sort(key=lambda x: x["score"], reverse=True)

top_3_hits = scored_hits[:3]

context_text = ""
for i, item in enumerate (top_3_hits):
    text = item["hit"].payload['content']
    context_text += f"\n[Document {i+1}]\n{text}\n"

print("result")

system_prompt = """
### ROLE
You are a Professional Financial Analyst specializing in corporate report auditing. Your goal is to provide precise, data-driven answers based strictly on the provided context.

### TASK
Analyze the provided [Context] (which includes text, tables, and image descriptions) to answer the user's [Question]. 

### CONSTRAINTS
1. STRICT ADHERENCE: Answer ONLY using the information found in the [Context]. 
2. NO EXTERNAL KNOWLEDGE: Do not use your pre-trained knowledge or outside information.
3. NO HALLUCINATION: If the information is not explicitly stated in the context, respond exactly with: "I cannot find this information in the provided documents."
4. CITATION: You must append the source reference at the end of your response (e.g., [Document 1], [Table 2]).

### OUTPUT FORMAT
- Maintain a professional and objective tone.
- Use bullet points for financial figures or comparisons to ensure clarity.
- Ensure all numbers and currency units are accurate as per the context.
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Document (Context):\n{context_text}\n\n---\nQuestion: {question}"}
    ],
    temperature=0
)

print("---Answer:----")
print(response.choices[0].message.content)