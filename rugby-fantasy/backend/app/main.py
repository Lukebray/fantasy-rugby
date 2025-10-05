from fastapi import FastAPI
from .auth.routes import router as auth_router

app = FastAPI(title="Rugby Fantasy API", version="1.0.0")

# Include authentication routes
app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"message": "Rugby Fantasy API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}