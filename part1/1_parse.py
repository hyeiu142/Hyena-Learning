import os
from dotenv import load_dotenv
from llama_parse import LlamaParse

load_dotenv()

parser = LlamaParse(
    result_type="markdown", 
    verbose=True
)

file_path = "report_ex/report.pdf"

print(f"Begin read file with LlamaParse, lp read file {file_path}...")

documents = parser.load_data(file_path)

output_md = "result.md"

with open(output_md, "w", encoding="utf-8") as f:
    for doc in documents: 
        f.write(doc.text + "\n\n")

print(f"Write file {output_md} success!")
