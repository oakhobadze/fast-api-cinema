# Entry point
from fastapi import FastAPI
from app.routers import movies

app = FastAPI()

app.include_router(movies.router)