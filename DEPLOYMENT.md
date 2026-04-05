# Streamlit Cloud Deployment Instructions

## Setup

1. **Push to GitHub**: Make sure your project is pushed to GitHub

2. **Add to Streamlit Cloud**:
   - Go to [Streamlit Community Cloud](https://streamlit.io/cloud)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository: `pdf-reader-RAG`
   - Main file: `web_app.py`
   - Python version: 3.10+

3. **Add Secrets** (Important!):
   - In the Streamlit Cloud app dashboard, go to "Settings" → "Secrets"
   - Add your OpenAI API key:
   ```
   OPENAI_API_KEY = "sk-proj-..."
   ```
   - Click "Save"

4. **Deploy**:
   - Your app will automatically deploy
   - It will be available at: `https://pdf-reader-rag-yourname.streamlit.app`

## Important

- Never commit `.env` files with real API keys to GitHub
- Use Streamlit Secrets instead for cloud deployment
- The app automatically detects if it's running on Streamlit Cloud and uses the appropriate secret storage
