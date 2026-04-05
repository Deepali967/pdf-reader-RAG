import argparse
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.tools import DuckDuckGoSearchRun

# Try to import streamlit (for Streamlit Cloud support)
try:
    import streamlit as st
    IS_STREAMLIT = True
except ImportError:
    IS_STREAMLIT = False


def load_environment():
    """Load environment variables from .env or Streamlit secrets."""
    load_dotenv()
    
    # Try to get API key from Streamlit secrets first (Streamlit Cloud), then from .env
    if IS_STREAMLIT:
        try:
            api_key = st.secrets.get("OPENAI_API_KEY")
        except:
            api_key = os.getenv("OPENAI_API_KEY")
    else:
        api_key = os.getenv("OPENAI_API_KEY")
    
    config = {
        "OPENAI_API_KEY": api_key,
    }
    if not config["OPENAI_API_KEY"]:
        raise ValueError("OPENAI_API_KEY is required. Set it in .env or the environment.")
    return config


def load_pdf_documents(pdf_path: str):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    print(f"Loaded {len(documents)} document chunks from {pdf_path}")
    return documents


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
    )
    return splitter.split_documents(documents)


def ingest_pdf(pdf_path: str, config: dict):
    documents = load_pdf_documents(pdf_path)
    documents = split_documents(documents)

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)
    print(f"Ingested {len(documents)} document chunks into FAISS.")
    return vectorstore


def query_pdf(vectorstore, question: str, config: dict):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}
Answer:"""
    prompt = PromptTemplate.from_template(template)

    qa_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | OpenAI(temperature=0.0)
        | StrOutputParser()
    )

    answer = qa_chain.invoke(question)
    
    # Check if answer indicates no knowledge
    if "don't know" in answer.lower() or "i don't know" in answer.lower():
        # Fallback to web search
        search = DuckDuckGoSearchRun()
        search_results = search.run(question)
        
        web_template = """Use the following web search results to answer the question. If you still don't know, say so.

Web results: {web_results}

Question: {question}
Answer:"""
        web_prompt = PromptTemplate.from_template(web_template)
        
        web_chain = (
            {"web_results": RunnablePassthrough(), "question": RunnablePassthrough()}
            | web_prompt
            | OpenAI(temperature=0.0)
            | StrOutputParser()
        )
        
        answer = web_chain.invoke({"web_results": search_results, "question": question})
        answer = f"Answer not found in PDF. From web search:\n{answer}"
    
    return answer


def main() -> None:
    parser = argparse.ArgumentParser(description="PDF QA bot using LangChain + FAISS")
    subparsers = parser.add_subparsers(dest="command")

    ingest_parser = subparsers.add_parser("ingest", help="Ingest a PDF into FAISS")
    ingest_parser.add_argument("pdf_path", help="Path to the PDF file to ingest")

    query_parser = subparsers.add_parser("query", help="Ask a question from the ingested PDFs")
    query_parser.add_argument("question", help="The question to ask")

    args = parser.parse_args()
    config = load_environment()

    if args.command == "ingest":
        vectorstore = ingest_pdf(args.pdf_path, config)
        vectorstore.save_local("faiss_index")
        print("Vectorstore saved to faiss_index")
    elif args.command == "query":
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        answer = query_pdf(vectorstore, args.question, config)
        print("\n--- Answer ---")
        print(answer)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
 