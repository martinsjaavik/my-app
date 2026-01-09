from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.puzzles import router as puzzles_router
from app.api.v1.games import router as games_router
from app.api.v1.ai import router as ai_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router)
api_router.include_router(puzzles_router)
api_router.include_router(games_router)
api_router.include_router(ai_router)
