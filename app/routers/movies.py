# Movie router will go here
from fastapi import APIRouter

router = APIRouter(prefix='/movies', tags=['Movies'])

@router.get('/')
def get_movies():
    return {'message': 'List of movies'}