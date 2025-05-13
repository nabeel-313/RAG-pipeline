from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from typing import List
import os
import shutil
from ChatPDF.pipline.data_pipeline import RAGPipeLine

# app = FastAPI()

# UPLOAD_DIR = "data"
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# # Setup for rendering templates
# templates = Jinja2Templates(directory="templates")

# @app.get("/", response_class=HTMLResponse)
# async def home(request: Request):
#     return templates.TemplateResponse("upload.html", {"request": request})

# @app.post("/fileupload")
# async def upload_files(files: List[UploadFile] = File(...)):
#     saved_files = []

#     for file in files:
#         if file.content_type != "application/pdf":
#             return JSONResponse(status_code=400, content={"error": f"{file.filename} is not a PDF."})

#         file_path = os.path.join(UPLOAD_DIR, file.filename)

#         with open(file_path, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)

#         saved_files.append(file.filename)

#     return {"message": "Files uploaded", "files": saved_files}

rag_pipeline = RAGPipeLine()
rag_pipeline.start_data_loading()