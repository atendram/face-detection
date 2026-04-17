from insightface.app import FaceAnalysis
import cv2
import numpy as np

app = FaceAnalysis()
app.prepare(ctx_id=0)  # 0 = GPU, -1 = CPU


def get_embedding(image_path):
    img = cv2.imread(image_path)
    faces = app.get(img)

    if len(faces) == 0:
        return None

    return faces[0].embedding.tolist()   # ✅ FIX

def compare_faces(emb1, emb2):
    emb1 = np.array(emb1)
    emb2 = np.array(emb2)

    distance = np.linalg.norm(emb1 - emb2)

    return distance