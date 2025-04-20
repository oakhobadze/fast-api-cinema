from fastapi import FastAPI
from app.core.database import Base, engine
from app.movies.routers import router as movies_router
from app.user.routers import router as user_router
from app.cart.routers import router as cart_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Cinema!"}

app.include_router(movies_router)
app.include_router(user_router)
app.include_router(cart_router)

