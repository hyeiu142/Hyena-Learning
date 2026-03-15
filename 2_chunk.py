from langchain_text_splitters import MarkdownTextSplitter

input_md = "result.md"
with open(input_md, "r", encoding="utf-8") as f: 
    text_content = f.read()

splitter = MarkdownTextSplitter(
    chunk_size=1000, 
    chunk_overlap=200
)

chunks=splitter.create_documents([text_content])

print(f"From original file, we turn into {len(chunks)} chunks")
print("-" * 50)

for i in range(5):
    print(f"\n chunk {i+1} (length: {len(chunks[i].page_content)} tokens)")
    print(chunks[i].page_content)
