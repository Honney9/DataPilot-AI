# app/api/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.upload import router as upload_router
from app.routes.data import router as data_router
from app.routes.visualization import router as viz_router
from app.routes.insights import router as insights_router
from app.routes.chat import router as chat_router
from app.routes.report import router as report_router
app = FastAPI()

# ✅ CORS (IMPORTANT for React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(data_router)
app.include_router(viz_router)
app.include_router(insights_router)
app.include_router(chat_router)
app.include_router(report_router)


@app.get("/health")
def health():
    return {"status": "ok"}