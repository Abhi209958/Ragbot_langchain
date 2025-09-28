import os
import uuid
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.api.routes import router

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Create FastAPI app
app = FastAPI(
    title="RAG Bot - Enhanced Multi-Document Q&A",
    description="A sophisticated RAG bot with multi-PDF support and modular architecture",
    version="2.0.0"
)

# Add session middleware (add this before CORS middleware)
app.add_middleware(SessionMiddleware, secret_key="your-secret-key-change-this-in-production")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

def get_session_id(request: Request) -> str:
    """Get or create a session ID for the user"""
    if "session_id" not in request.session:
        request.session["session_id"] = str(uuid.uuid4())
    return request.session["session_id"]

# Include API routes with session dependency
app.include_router(router, prefix="/api", tags=["RAG Bot"])

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Ensure user has a session ID
    get_session_id(request)
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "RAG Bot is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
