from fastapi import FastAPI
from app.core.database import Base, engine
from app.movies.routers import router as movies_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Cinema!"}

app.include_router(movies_router)
