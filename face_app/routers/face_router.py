import json
import os
import shutil
from fastapi import APIRouter, File, Form, UploadFile
from face_app.services.checkin_service import  check_visitor
from face_app.services.face_service import get_single_visitor, getCheckVisitor, upsert_visitor,get_all_visitor
from face_app.services.faiss_service import add_to_index
import face_app.services.faiss_service as faiss_service
from face_app.utils.face_detection import get_embedding
import uuid
router = APIRouter(prefix="/users", tags=["Users"])


UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# upload_face to user in the visitor master
@router.post("/upload_face")
async def upload_face(id: int, file: UploadFile):
    file_path = f"{UPLOAD_FOLDER}/{uuid.uuid4()}_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    embedding = get_embedding(file_path)
    if embedding is None:
        return {"error": "No face detected"}
    message = upsert_visitor(id,embedding)
    visitor = get_single_visitor(id)
    if visitor:
        add_to_index(visitor)
    return message


# detect the face from the visitor master
@router.post("/verify_face")
async def verify_face(file: UploadFile):

    try:
        file_path = f"{UPLOAD_FOLDER}/{uuid.uuid4()}_{file.filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        new_embedding = get_embedding(file_path)
   
        if new_embedding is None:
            return {"status":1 ,"error": "No face detected"}
        result = check_visitor(faiss_service.faiss_index,faiss_service.faiss_data,new_embedding)
        if result["status"] ==  1:
            return result
        return {"status":0,"message": "Visitor Not Found","embedding": new_embedding.tolist() if hasattr(new_embedding, "tolist") else new_embedding}

    except Exception as e:
        return {"error": str(e)}
    
@router.post("/check_visitor")
def checkin_out(
    checkType: str = Form(...),
    checkBy: int = Form(...),
    file: UploadFile = File(...)
):
    try:
        file_path = f"{UPLOAD_FOLDER}/{uuid.uuid4()}_{file.filename}"

        print("Saving file...")
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print("File saved:", file_path)
        print("Exists:", os.path.exists(file_path))
        new_embedding = get_embedding(file_path)

        if new_embedding is None:
            return {"status": 0, "error": "no face detected"}

        result = check_visitor(
            faiss_service.faiss_index,
            faiss_service.faiss_data,
            new_embedding
        )

        if result["status"] != 1:
            return result

        visitor = result["data"]

        return getCheckVisitor(checkBy, checkType, visitor)

    except Exception as e:
        return {"error": str(e)}


        