from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List
import os
from pydantic import BaseModel
import shutil
from ChatPDF.pipline.data_pipeline import RAGPipeLine
from ChatPDF.pipline.retrival_pipeline import RetrievalPipeline
from ChatPDF.exception import RAGException


app = FastAPI()
# CORS setup for local frontend-backend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for dev. Restrict in prod.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Set template and static file folders
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
UPLOAD_DIR = "data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Setup for rendering templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/fileupload")
async def upload_files(files: List[UploadFile] = File(...)):
    saved_files = []

    for file in files:
        if file.content_type != "application/pdf":
            return JSONResponse(status_code=400, content={"error": f"{file.filename} is not a PDF."})

        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        saved_files.append(file.filename)

    return {"message": "Files uploaded", "files": saved_files}

rag_pipeline = RAGPipeLine()
#loaded_data = rag_pipeline.run_pipeline()  
#chunks = rag_pipeline.start_data_chunking(loaded_data)
retriver = RetrievalPipeline()
@app.get("/chat", response_class=HTMLResponse)
async def serve_chat_ui():
    return FileResponse("templates/index.html")
class ChatRequest(BaseModel):
    data: str
    
# Endpoint for chat interaction
@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    try:
        response = retriver.chat(req.data)
        print("---->>>>",response.get("answer"))
        return JSONResponse(content={"response": True, "message": response.get("answer")})
    except Exception as e:
        return JSONResponse(content={"response": False, "message": str(e)})
#print("💬 Start chatting with Gemini. Type 'exit' to stop.")
# while True:
#     query = input("\n🧠 You: ")
#     if query.lower() in ["exit", "quit"]:
#         print("👋 Bye!")
#         break

#     response = retriver.chat(query)
#     print(f"\n🤖 Gemini:\n{response}")