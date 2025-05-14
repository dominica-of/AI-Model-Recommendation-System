# GenAI-Powered Model Recommender System

This project implements a Retrieval-Augmented Generation (RAG) pipeline to recommend AI models using Large Language Models (LLMs) and structured scoring. It serves as the technical foundation for the Master’s thesis “Development and Evaluation of a GenAI Recommender System for AI Model Selection” by Abena Amanfo (Lucerne University of Applied Sciences and Arts, Master of Science in Applied Information and Data Science (MScIDS), Spring Semester, 2025).

## Project Structure

```
thesis_root/
├── app/
│   └── streamlit_app.py              # Web UI (Streamlit)
├── backend/
│   ├── chromadb_api.py              # FastAPI endpoint to query ChromaDB
│   ├── insert_data.py               # Loads structured data into PostgreSQL
│   ├── insert_chromadb.py          # Loads semantic data into ChromaDB
│   ├── metadata_fetcher.py         # DB interaction class for PostgreSQL
│   ├── remote_retriever.py         # Calls external ChromaDB retriever API
│   ├── retriever.py                # Retrieval implementation from local ChromaDB instance
│   ├── prompt_template.py          # Constructs structured LLM prompt
│   └── llm_inference.py            # GPT-4/3.5-based inference wrapper
├── data/
│   ├── model_metadata_final.csv    # Structured model metadata (latest)
│   ├── model_metadata_chromadb.csv # Processed text fields for embedding
├── requirements.txt                # Python dependency list
└── README.md                       # Project documentation
```

## Key Features

- **GenAI-Powered Recommendation**: GPT-4-turbo generates justifiable model suggestions.
- **RAG Architecture**: Combines structured PostgreSQL metadata with semantically retrieved text from ChromaDB.
- **Multi-Criteria Scoring Engine**: Evaluates models based on performance, popularity, licensing, hardware compatibility, documentation, and institutional credibility.
- **Interactive Web UI**: Built with Streamlit to allow users to describe projects and receive real-time recommendations.


## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Insert Data into Databases

- **PostgreSQL (Structured):**

```bash
python backend/insert_data.py
```

- **ChromaDB (Embeddings):**

```bash
python backend/insert_chromadb.py
```

> ⚠️ Ensure both PostgreSQL and ChromaDB services are running locally or available via remote endpoints.

### 3. Launch Web Interface

```bash
streamlit run app/streamlit_app.py
```

## 💬 Example Prompt

> Describe your project , e.g.:
>
> *"I need a model that performs named entity recognition on legal documents using PyTorch and must be open-source."*

The system retrieves the top candidate models from ChromaDB, fetches metadata from PostgreSQL, and generates a reasoned recommendation using GPT-4.

## 🔐 Data Security & Deployment

- PostgreSQL and ChromaDB operate in isolated environments with role-based access.
- API keys are stored securely via `.env` or `.streamlit/secrets.toml`.

## Scoring Engine Explanation

Navigate to the **"Scoring Engine Explanation"** tab in the Streamlit UI to:

- View individual scoring formulas.
- Explore the impact of each dimension.
- Understand how models are ranked and selected.

## References

This system is grounded in research on:

- Recommender systems (Johnson & Lee, 2023)
- Large language models and prompt engineering (Brown et al., 2023)
- Decision support systems (Williams, 2024)
- Industry needs in model selection (Gartner, McKinsey, Hugging Face, PapersWithCode)

## Academic Attribution

**Author:** Abena Amanfo  
**Thesis:** *Development and Evaluation of a GenAI Recommender System for AI Model Selection*  
**Supervisors:** Prof. Dr. Luis Terán, José Mancera, Zeeshan Khalid  
**Institution:** Lucerne University of Applied Sciences and Arts  
**Program:** MSc Applied Information and Data Science  
**Semester:** Spring 2025
