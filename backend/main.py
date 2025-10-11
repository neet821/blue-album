# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # 导入 CORS 中间件

app = FastAPI()

# --- CORS 配置开始 ---
# 定义允许访问的源列表，这里是 Vue 开发服务器的地址
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许访问的源
    allow_credentials=True, # 支持 cookie
    allow_methods=["*"],    # 允许所有方法
    allow_headers=["*"],    # 允许所有请求头
)
# --- CORS 配置结束 ---


@app.get("/")
def read_root():
    return {"message": "FastAPI backend is running"}

@app.get("/api/test")
def test_connection():
    return {"message": "成功！消息来自 FastAPI 后端！"}

# ... 您其他的 API 路由 ...