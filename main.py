import uvicorn
from fastapi import FastAPI, Response
from fastapi.responses import RedirectResponse
from fastapi.openapi.docs import get_swagger_ui_html
from pathlib import Path
# from starlette.middleware.base import BaseHTTPMiddleware

# from api.routers.dashboard.dashboard_router import router as dashboard_router
PATH_APP_PY = Path(__file__)
PATH_PROJECT = PATH_APP_PY.parent

app = FastAPI(docs_url=None)  #remove default /docs endpoint

# swagger tags -> fast api cdn 의존성 제거를 위해 custom

@app.get('/', tags=['swagger'], include_in_schema=False)
def index():    
    return RedirectResponse('/docs')

@app.get('/docs', tags=['swagger'], include_in_schema=False)
def swagger_docs():    
    rsp = get_swagger_ui_html(                                          
                                openapi_url = "/openapi.json",                                   
                                title = "MetaFactory Swagger",                                    
                                swagger_css_url="/swagger_css",                                    
                                swagger_js_url = "/swagger_js"                        
                            )    
    return rsp

@app.get('/swagger_css', tags=['swagger'], include_in_schema=False)
def swagger_css():    
    with open(Path(PATH_PROJECT,"swagger/swagger-ui.css"),'rt',encoding='utf-8') as f:        
        swagger_css = f.read()    
    return Response(swagger_css,headers={"Content-type":"text/css"})

@app.get('/swagger_js', tags=['swagger'], include_in_schema=False)
def swagger_js():   
    with open(Path(PATH_PROJECT,"swagger/swagger-ui.js"),'rt',encoding='utf-8') as f:        
        swagger_js = f.read()    
    return Response(swagger_js,headers={"Content-type":"text/javascript"})

@app.get("/health-check") 
async def root():     
    return {"result": "Run"} 

# app.add_middleware(BaseHTTPMiddleware)
# app.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"], include_in_schema=True)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8086, reload=True)