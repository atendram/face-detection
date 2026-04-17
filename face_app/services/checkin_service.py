import json

from face_app.utils.face_detection import compare_faces

import faiss
import numpy as np
import json

# def build_faiss_index(visitors):
#     embeddings = []
#     data = []

#     for visitor in visitors:
#         emb_str = visitor["embedding"]

#         if not emb_str or emb_str == "null":
#             continue

#         try:
#             emb = json.loads(emb_str)
#             embeddings.append(emb)

#             # ✅ store FULL visitor
#             data.append(visitor)

#         except:
#             continue

#     if len(embeddings) == 0:
#         return None, None

#     embeddings = np.array(embeddings).astype('float32')

#     dimension = embeddings.shape[1]

#     index = faiss.IndexFlatL2(dimension)
#     index.add(embeddings)

#     return index, data   # ✅ return full data


def check_visitor(index, data, new_embedding):
    if index is None:
        return {"status": 0, "message": "No data in index"}

    query = np.array([new_embedding]).astype('float32')

    distances, indices = index.search(query, k=1)

    best_distance = distances[0][0]
    best_index = indices[0][0]

    print("FAISS distance:", best_distance)

    if best_distance < 1.0:
        visitor = data[best_index]
        visitor_copy = dict(visitor)

        return {
            "status": 1,
            "message": "Visitor Found",
            "data": visitor_copy
        }

    return {"status": 0, "message": "Visitor Not Found"}