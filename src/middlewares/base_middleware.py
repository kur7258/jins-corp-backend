from fastapi import FastAPI, Request
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)

# CORS 허용을 위한 middleware (TODO 클라이언트 서버 생성 시 연결 필요)
# @app.middleware("http")
# async def add_cors_headers(request, call_next):
#     response = await call_next(request)
#     response.headers["Access-Control-Allow-Origin"] = "*"
#     return response

# 모든 api 호출에 대한 logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logging.info(f"Request URL: {request.url.path}")
    response = await call_next(request)
    logging.info(f"Response status code: {response.status_code}")
    return response