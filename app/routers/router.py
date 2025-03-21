from fastapi import APIRouter

from app.utils.settings import settings
from app.routers import token, users, manufacturers


# Arquivo criado para unificar as rotas dos endpoints
# Seguindo o principio DRY (Dont Repeat Yourself), escrevemos o prefixo "/api/v1" apenas uma vez
# Outra vantagem é não que não vamos poluir o arquivo main.py com inúmeros imports e linhas para incluir as rotas
router = APIRouter(
    prefix=settings.URI_PREFIX
)

router.include_router(token.router)
router.include_router(users.router)
router.include_router(manufacturers.router)
