from pathlib import Path
import sys
from dotenv import load_dotenv

project_root = Path(__file__).resolve().parent.parent
load_dotenv(project_root / ".env")


# プロジェクトルートを追加
sys.path.append(str(Path(__file__).resolve().parent.parent))

from tools.pdf_parser import PDFParser
from vectorstore.llamaindex.builder import LlamaIndexBuilder
from vectorstore.llamaindex.retriever import LlamaRetriever

parser = PDFParser()

pdf_path = "papers/paper.pdf"

pages = parser.extract_pages(pdf_path)
chunks = parser.chunk_pages(pages)

builder = LlamaIndexBuilder()
index = builder.build(chunks)

retriever = LlamaRetriever(index)

docs = retriever.retrieve("What is HippoRAG?")

for node in docs:

    print("=" * 80)

    print(f"Score : {node.score:.4f}")

    print(node.metadata)

    print(node.text)