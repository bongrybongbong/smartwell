from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import json
import os

app = FastAPI()

# 기본 홈 라우트 (테스트용)
@app.get("/")
async def read_root():
    return {"message": "🚀 FastAPI 서버 정상 작동 중입니다! /upload_result 또는 /get_latest_result 사용하세요."}

# POST → Colab에서 json 업로드
@app.post("/upload_result")
async def upload_result(request: Request):
    data = await request.json()
    os.makedirs("static/results", exist_ok=True)
    with open("static/results/latest_result.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return {"message": "✅ Result uploaded successfully"}

# GET → Streamlit에서 최신 json 가져오기
@app.get("/get_latest_result")
async def get_latest_result():
    try:
        with open("static/results/latest_result.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
