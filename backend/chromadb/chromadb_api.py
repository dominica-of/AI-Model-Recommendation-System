from fastapi import FastAPI
from pydantic import BaseModel
import requests
from sentence_transformers import SentenceTransformer

app = FastAPI()
embedder = SentenceTransformer('all-MiniLM-L6-v2')

CHROMA_API = "https://chroma-server-dj4p.onrender.com"  

class QueryRequest(BaseModel):
    query_text: str
    top_k: int = 5

class QueryResponse(BaseModel):
    ids: list

@app.post("/query", response_model=QueryResponse)
def query_vectorstore(request: QueryRequest):
    embedding = embedder.encode([request.query_text])
    response = requests.post(
        f"{CHROMA_API}/api/v1/query",
        json={"query_embeddings": embedding.tolist(), "n_results": request.top_k}
    )
    result = response.json()
    return QueryResponse(ids=result.get("ids", []))

@app.get("/collection")
def get_collection_data():
    response = requests.post(f"{CHROMA_API}/api/v1/get", json={"include": ["documents"]})
    return response.json()
