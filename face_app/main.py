from fastapi import FastAPI
from face_app.routers import face_router
from fastapi.middleware.cors import CORSMiddleware
from face_app.services.faiss_service import build_faiss_index
from face_app.services.face_service import get_all_visitor
app = FastAPI()
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Response-Time-Ms"] 
)


@app.on_event("startup")
def load_index():
    visitors = get_all_visitor()
    build_faiss_index(visitors)

app.include_router(face_router.router)