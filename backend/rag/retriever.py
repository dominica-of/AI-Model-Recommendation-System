import requests

class Retriever:
    def retrieve(self, query_text):
        response = requests.post(
            "https://chroma-server-dj4p.onrender.com/query",
            json={"query_text": query_text}
        )
        return response.json()["ids"]
