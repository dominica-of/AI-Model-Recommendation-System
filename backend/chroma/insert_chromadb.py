import chromadb
from sentence_transformers import SentenceTransformer
import pandas as pd

def insert_chromadb():
    client = chromadb.HttpClient(host='localhost', port=8000)
    collection = client.get_or_create_collection(name='model_data')

    df_chroma = pd.read_csv('/Users/dom/Desktop/Thesis/thesis_root/data/prepropessed data/model_metadata_chromadb.csv')
    embedder = SentenceTransformer('all-MiniLM-L6-v2')

    embeddings = embedder.encode(df_chroma['composite_text'].tolist(), show_progress_bar=True)

    for idx, row in df_chroma.iterrows():
        collection.add(ids=row['Model'], documents=row['composite_text'], embeddings=embeddings[idx])

    print("Data saved to ChromaDB.")

if __name__ == '__main__':
    insert_chromadb()
