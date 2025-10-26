# Agentic RAG Chatbot

This project is a Retrieval-Augmented Generation (RAG) chatbot powered by LangChain, Streamlit, and Ollama. It uses a local Chroma vector database to store and retrieve document embeddings, enabling context-aware responses to user queries.

## Features
- **Streamlit UI**: Interactive chat interface for user interaction.
- **LangChain Integration**: Uses LangChain agents, prompts, and tools for flexible RAG workflows.
- **Ollama Embeddings**: Embedding model for document vectorization.
- **Chroma Vector Store**: Local vector database for fast similarity search.
- **Multi-format Data Ingestion**: Supports TXT, PDF, DOCX, CSV, and JSON files for knowledge ingestion.
- **Environment Configuration**: Uses `.env` for model and database settings.

## File Structure
- `chatbot.py`: Main Streamlit app for chat UI and agent execution.
- `RAG.py`: Data ingestion, chunking, embedding, and vector store population.
- `chroma_db/`: Local Chroma database files.
- `data/`: Folder for source documents (e.g., `cooking.txt`).
- `.env`: Environment variables for model/database configuration.

## Setup
1. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```
2. **Configure environment**:
   - Create a `.env` file with the following variables:
     ```env
     EMBEDDING_MODEL=your-embedding-model
     CHAT_MODEL=your-chat-model
     MODEL_PROVIDER=your-model-provider
     COLLECTION_NAME=your-collection-name
     DATABASE_LOCATION=./chroma_db
     DATASET_STORAGE_FOLDER=./data
     ```
3. **Add data**:
   - Place TXT, PDF, DOCX, CSV, or JSON files in the `data/` folder.

4. **Run ingestion**:
   ```powershell
   python RAG.py
   ```
   This will process and embed your documents into the Chroma vector store.

5. **Start the chatbot**:
   ```powershell
   streamlit run chatbot.py
   ```


## Supported RAG Models
This chatbot supports any model available via Ollama and LangChain that provides embeddings and chat capabilities. Some popular models include:

- **Ollama**:
   - llama
   - mistral
   - phi3
   - codellama
   - gemma
   - dbrx
   - mixtral
   - orca-mini
   - vicuna
   - openchat
   - neural-chat
   - dolphin-mixtral
   - qwen
   - starling-lm
   - and more (see [Ollama models list](https://ollama.com/library))

- **LangChain**:
   - Any model supported by LangChain's chat and embedding interfaces (OpenAI, HuggingFace, etc.)

Specify your desired models in the `.env` file:
```env
EMBEDDING_MODEL=llama2
CHAT_MODEL=llama2
MODEL_PROVIDER=ollama
```

## Usage
- Enter your questions in the chat interface. The agent will retrieve relevant information from the ingested documents and respond with sources.

## License
MIT
