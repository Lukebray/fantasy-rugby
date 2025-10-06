from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .auth.routes import router as auth_router
from .routers import users, leagues, squads, transfers, stats

app = FastAPI(title="Rugby Fantasy API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Include authentication routes
app.include_router(auth_router)
app.include_router(leagues.router)

@app.get("/")
def read_root():
    return {"message": "Rugby Fantasy API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}