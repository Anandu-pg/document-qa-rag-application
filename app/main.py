from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.agents.graph import app_graph
from app.utils.document_loader import load_and_split_document
from app.utils.vectorstore import get_vectorstore
import shutil
from pathlib import Path
import uuid

app = FastAPI(title="Document QA Agent", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files only if directory exists
static_dir = Path("static")
if static_dir.exists() and static_dir.is_dir():
    app.mount("/static", StaticFiles(directory="static"), name="static")
    
    @app.get("/", include_in_schema=False)
    async def read_root():
        return FileResponse("static/index.html")
else:
    @app.get("/")
    async def read_root():
        return {
            "message": "Document QA Agent API",
            "status": "running",
            "endpoints": {
                "upload": "/upload-document/",
                "ask": "/ask/",
                "health": "/health",
                "docs": "/docs"
            }
        }

# Request/Response models
class QuestionRequest(BaseModel):
    question: str

class QuestionResponse(BaseModel):
    question: str
    answer: str
    relevance_score: float

@app.post("/upload-document/")
async def upload_document(file: UploadFile = File(...)):
    """Upload and ingest a document into the vector store"""
    try:
        file_id = str(uuid.uuid4())
        file_path = f"/tmp/{file_id}_{file.filename}"
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        splits = load_and_split_document(file_path)
        vectorstore = get_vectorstore()
        vectorstore.add_documents(splits)
        Path(file_path).unlink()
        
        return JSONResponse(content={
            "message": f"Document '{file.filename}' ingested successfully",
            "chunks": len(splits)
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask/", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """Ask a question about ingested documents"""
    try:
        result = app_graph.invoke({
            "question": request.question,
            "context": [],
            "answer": "",
            "relevance_score": 0.0
        })
        
        if result["relevance_score"] <= 0.5:
            return QuestionResponse(
                question=request.question,
                answer="I couldn't find relevant information to answer your question.",
                relevance_score=result["relevance_score"]
            )
        
        return QuestionResponse(
            question=request.question,
            answer=result["answer"],
            relevance_score=result["relevance_score"]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
