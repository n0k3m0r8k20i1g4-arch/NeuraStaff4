# backend.py
from fastapi import FastAPI, HTTPException, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

# =========================
# DB設定
# =========================
DATABASE_URL = "sqlite:///./tasks.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(bind=engine)

# =========================
# FastAPI設定
# =========================
app = FastAPI(title="AI社員 Workspace Pro API")

# CORS設定（フロント用）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 必要に応じてフロントのURLに変更
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Pydanticモデル
# =========================
class TaskCreate(BaseModel):
    type: str
    content: str

class TaskOut(BaseModel):
    id: int
    type: str
    content: str
    created_at: datetime.datetime

# =========================
# APIルート
# =========================
@app.get("/tasks", response_model=List[TaskOut])
def get_tasks():
    db = SessionLocal()
    tasks = db.query(Task).order_by(Task.created_at.desc()).all()
    db.close()
    return tasks

@app.post("/tasks", response_model=TaskOut)
def create_task(task: TaskCreate):
    db = SessionLocal()
    db_task = Task(type=task.type, content=task.content)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    db.close()
    return db_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        db.close()
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    db.close()
    return {"detail": "Task deleted"}

# 音声入力（音声ファイル→テキスト変換、仮）
@app.post("/speech-to-text")
def speech_to_text(file: UploadFile):
    # 実際にはWhisperやOpenAI APIなどを使う
    filename = file.filename
    content = f"音声ファイル {filename} を解析してテキスト化しました（仮）"
    return {"text": content}
