# PDF QA Bot with LangChain + FAISS (RAG)

This project shows how to ingest PDF documents into a FAISS vector database and answer user questions using Retrieval-Augmented Generation (RAG). If the answer isn't found in the PDF, it falls back to web search.

## Features
- Load PDF files
- Split and embed text into FAISS
- Use OpenAI embeddings and LLM completion
- Answer questions with retrieval-based QA
- Fallback to web search if answer not in PDF

## Requirements
- Python 3.10+
- OpenAI API key

## Install
1. Create a virtual environment and activate it:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set environment variables in a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
```

## Usage

### Web Chat Interface (Recommended)

1. Start the web app:
   ```bash
   streamlit run web_app.py
   ```

2. Open your browser to `http://localhost:8501`

3. Upload a PDF file and click "Ingest PDF"

4. Ask questions in the chat interface

The bot will first search the PDF. If no relevant information is found, it will perform a web search and provide an answer based on that.

### Command Line Interface

#### Ingest a PDF

```bash
python app.py ingest /path/to/file.pdf
```

### Ask a question

```bash
python app.py query "What is the main topic of the document?"
```

### Notes
- The bot uses OpenAI embeddings and OpenAI LLM by default.
- You can reuse the same `WEAVIATE_CLASS` for multiple PDF files.
