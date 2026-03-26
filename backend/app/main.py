from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import student, statistics, ai
from app.core.database import engine, Base

# 创建表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="大学生就业信息智能分析平台",
    description="为学生、辅导员、学校管理层提供就业数据分析服务",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(student.router, prefix="/api/v1")
app.include_router(statistics.router, prefix="/api/v1")
app.include_router(ai.router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "大学生就业信息智能分析平台 API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}