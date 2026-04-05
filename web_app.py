import streamlit as st
import tempfile
import os
from pathlib import Path

# Import functions from app.py
from app import load_environment, ingest_pdf, query_pdf

def main():
    st.title("PDF QA Chat Bot")
    st.markdown("Upload a PDF and ask questions about its content.")

    # Load environment config
    try:
        config = load_environment()
    except ValueError as e:
        st.error(str(e))
        st.stop()

    # File uploader
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        # Save uploaded file to temp location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            pdf_path = tmp_file.name

        # Ingest button
        if st.button("Ingest PDF"):
            with st.spinner("Ingesting PDF into FAISS..."):
                try:
                    vectorstore = ingest_pdf(pdf_path, config)
                    st.session_state.vectorstore = vectorstore
                    st.success("PDF ingested successfully!")
                except Exception as e:
                    st.error(f"Error ingesting PDF: {str(e)}")

        # Clean up temp file
        os.unlink(pdf_path)

    # Chat interface
    if "vectorstore" in st.session_state:
        st.subheader("Ask a Question")
        question = st.text_input("Enter your question:")

        if st.button("Ask"):
            if question.strip():
                with st.spinner("Generating answer..."):
                    try:
                        answer = query_pdf(st.session_state.vectorstore, question, config)
                        st.write("**Answer:**")
                        st.write(answer)
                    except Exception as e:
                        st.error(f"Error querying: {str(e)}")
            else:
                st.warning("Please enter a question.")
    else:
        st.info("Please upload and ingest a PDF first.")

if __name__ == "__main__":
    main()