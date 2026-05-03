from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api import auth, classes, records, students
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="学生信息管理系统", version="1.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(classes.router)
app.include_router(students.router)
app.include_router(records.router)
app.include_router(records.global_router)

# 生产模式：挂载前端构建产物（API 路由优先）
frontend_dir = Path(__file__).resolve().parent.parent.parent / "web" / "dist"
if frontend_dir.is_dir():
    app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")
