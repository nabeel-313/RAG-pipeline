import logging
import os
import shutil
from typing import List

from fastapi import FastAPI, File, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from ChatPDF.exception import RAGException
from ChatPDF.pipline.data_pipeline import RAGPipeLine
from ChatPDF.pipline.retrival_pipeline import RetrievalPipeline

# Initialize FastAPI app
app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# CORS setup for local frontend-backend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for dev. Restrict in prod.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set template and static file folders
UPLOAD_DIR = "data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    """Renders the homepage for file upload."""
    logger.info("Serving upload page.")
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/fileupload")
async def upload_files(files: List[UploadFile] = File(...)) -> JSONResponse:
    """
    Uploads PDF files to the server.

    Args:
        files (List[UploadFile]): List of PDF files uploaded by the user.

    Returns:
        JSONResponse: Upload status and list of saved files.
    """
    saved_files = []
    logger.info("Received %d file(s) for upload.", len(files))

    for file in files:
        if file.content_type != "application/pdf":
            logger.warning("File %s is not a PDF.", file.filename)
            return JSONResponse(status_code=400, content={"error": f"{file.filename} is not a PDF."})

        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info("Saved file: %s", file.filename)
        saved_files.append(file.filename)

    # to create and upload embedding uncomment next 3 lines
    # rag_pipeline = RAGPipeLine()
    # loaded_data = rag_pipeline.run_pipeline()  
    # chunks = rag_pipeline.start_data_chunking(loaded_data)

    return JSONResponse(content={"message": "Files uploaded", "files": saved_files})

# Initialize retrieval pipeline
retriver = RetrievalPipeline()

@app.get("/chat", response_class=HTMLResponse)
async def serve_chat_ui() -> FileResponse:
    """Serves the chat user interface page."""
    logger.info("Serving chat UI page.")
    return FileResponse("templates/index.html")

class ChatRequest(BaseModel):
    data: str

@app.post("/chat")
async def chat_endpoint(req: ChatRequest) -> JSONResponse:
    """
    Processes chat input from the user and returns a response from the chatbot.

    Args:
        req (ChatRequest): Request body containing user query.

    Returns:
        JSONResponse: Response from the retrieval pipeline.
    """
    logger.info("Received chat request: %s", req.data)
    try:
        response = retriver.chat(req.data)
        logger.info("Generated response: %s", response.get("answer"))
        return JSONResponse(content={"response": True, "message": response.get("answer")})
    except Exception as e:
        logger.error("Chat processing failed: %s", str(e))
        return JSONResponse(content={"response": False, "message": str(e)})