import faiss
import numpy as np
import json

faiss_index = None
faiss_data = []
def add_to_index(visitor):
    global faiss_index, faiss_data

    emb_str = visitor["embedding"]

    if not emb_str or emb_str == "null":
        return

    emb = json.loads(emb_str)
    emb = np.array([emb]).astype("float32")

    faiss_index.add(emb)
    faiss_data.append(visitor)

    print("FAISS updated +1")
    
def build_faiss_index(visitors):
    global faiss_index, faiss_data
    embeddings = []
    data = []
    for visitor in visitors:
        emb_str = visitor["embedding"]
        if not emb_str or emb_str == "null":
            continue
        try:
            emb = json.loads(emb_str)
            embeddings.append(emb)
            data.append(visitor)
        except:
            continue

    if not embeddings:
        return

    embeddings = np.array(embeddings).astype("float32")

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss_index = index
    faiss_data = data

    print("FAISS built:", len(data))
