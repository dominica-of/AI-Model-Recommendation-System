import requests

class RemoteRetriever:
    def __init__(self, base_url="https://chromadb-api.onrender.com"):
        self.base_url = base_url.rstrip("/")

    def retrieve(self, query_text, top_k=5):
        response = requests.post(
            f"{self.base_url}/query",
            json={"query_text": query_text, "top_k": top_k}
        )
        if response.status_code == 200:
            return response.json().get("ids", [])
        else:
            raise RuntimeError(f"Retriever failed: {response.text}")
