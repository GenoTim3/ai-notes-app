from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import your routes
from backend.routes import notes
from backend.routes import summarize

app = FastAPI(title="AI Notes App")

# CORS settings (allow your frontend to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your routers
app.include_router(notes.router, prefix="/notes", tags=["notes"])
app.include_router(summarize.router, prefix="/summarize", tags=["summarize"])

@app.get("/")
def root():
    return {"message": "AI Notes App backend is running!"}
