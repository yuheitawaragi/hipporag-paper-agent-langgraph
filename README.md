# Research Paper Search Agent

An AI-powered research paper search agent built with **LangGraph**, **OpenAI API**, and the **arXiv API**.

The application helps users search for research papers, retrieve relevant publications, and generate concise summaries using large language models.

## Features

* 🔍 Search research papers from arXiv
* 🤖 AI-powered paper summarization
* 📄 Automatic metadata extraction
* 💬 Natural language interaction
* ⚡ LangGraph-based agent workflow
* 🧠 OpenAI API integration
* 📚 Optimized for AI and Machine Learning literature

## Architecture

```text
User
   │
   ▼
LangGraph Agent
   │
   ├── Search Papers (arXiv API)
   ├── Retrieve Metadata
   ├── Summarize with OpenAI
   └── Generate Response
```

## Tech Stack

* Python
* LangGraph
* OpenAI API
* arXiv API
* Pydantic
* python-dotenv

## Installation

```bash
git clone https://github.com/yuheitawaragi/Research-Paper-Search-Agent.git

cd Research-Paper-Search-Agent

python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file:

```text
OPENAI_API_KEY=your_api_key
```

## Usage

Run the application:

```bash
python app.py
```

Example query:

> "Find recent GraphRAG papers published in 2025."

## Future Work

* GraphRAG integration
* HippoRAG support
* Semantic vector search
* Citation-aware retrieval
* Multi-agent workflow
* PDF download and analysis
* Local LLM support

## License

This project is released under the MIT License.

## Acknowledgements

* OpenAI
* LangGraph
* arXiv API






