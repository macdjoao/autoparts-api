from fastapi import APIRouter

from routes import users


# Arquivo criado para unificar as rotas dos endpoints
# Seguindo o principio DRY (Dont Repeat Yourself), escrevemos o prefixo "/api/v1" apenas uma vez
# Outra vantagem é não que não vamos poluir o arquivo main.py com inúmeros imports e linhas para incluir as rotas
router = APIRouter(
    prefix='/api/v1'
)

router.include_router(users.router)
