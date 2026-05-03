from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, classes, records, students
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="学生信息管理系统", version="1.0.0")

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


@app.get("/")
def root():
    return {"message": "学生信息管理系统 API"}
