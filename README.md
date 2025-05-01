thesis_root/
├── app/
│   └── streamlit_app.py          # Streamlit app entry point 
├── backend/
│   ├── main.py                  # FastAPI app entry point
│   ├── recommender.py           # Recommendation logic
│   ├── database.py              # Loads model data from CSV
│   ├── schemas.py               # Input validation models
│   └── insert_data.py           # Script to load data into PostgreSQL
├── data/
│   └── models.csv               # Dataset of AI models
└── requirements.txt             # Python dependencies
└── README.md                   # Project documentation





# GenAI Model Recommendation System (Streamlit + RAG)

This project implements a Retrieval-Augmented Generation pipeline for AI model recommendation.

## Modules

- `rag/retriever.py`: embedding + ChromaDB retrieval
- `rag/metadata_fetcher.py`: PostgreSQL metadata query
- `rag/prompt_template.py`: structured prompt generator
- `rag/llm_inference.py`: GPT-4 inference
- `app_streamlit.py`: frontend

## Run

```bash
streamlit run streamlit_app.py



#  'requirements.txt' contains the following dependencies:
# fastapi
# uvicorn
# pandas
# psycopg2
# pydantic
