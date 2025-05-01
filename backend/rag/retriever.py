import chromadb
from sentence_transformers import SentenceTransformer

class Retriever:
    def __init__(self, chroma_host='localhost', chroma_port=8000, embed_model='all-MiniLM-L6-v2'):
        self.client = chromadb.HttpClient(host='chroma-server-dj4p.onrender.com', port=443, ssl=True)
        self.collection = self.client.get_or_create_collection(name='model_data')
        self.embedder = SentenceTransformer(embed_model)

    def retrieve(self, query_text, top_k=5):
        query_embedding = self.embedder.encode([query_text])
        results = self.collection.query(query_embeddings=query_embedding, n_results=top_k)
        return results['ids']
