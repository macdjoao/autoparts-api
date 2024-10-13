from typing import List

from fastapi import APIRouter, HTTPException, status

from schemas import User
from models import users


router = APIRouter(
    prefix='/api/v1',
    tags=['Users']
)


# Padrão de nomenclatura dos endpoints: "/api/v1/resources". (O prefixo "/api/v1" é adicionado em router para diminuir repetição)
# "/" + nome do recurso (substantivo) em que a operação está sendo realizada, sem "/" no final.
# Tanto singular "/resource", quanto plural "/resources", são aceitos, mas é importante seguir o padrão escolhido para todos os endpoints.
@router.get(
    '/users',
    # Passar "-> List[User]" como retorno na assinatura da função teria o mesmo efeito que response_model
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary='Lista usuários',
    description='Lista todos os usuários cadastrados no sistema'
)
async def get_users():
    try:
        return users
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Internal Server Error'
        )


@router.get(
    '/users/{pk}',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Busca usuário',
    description='Busca um usuário cadastrado no sistema, baseado em sua chave primária'
)
# Padrão de nomenclatura das funções de endpoint: verbo http + recurso (no plural para listagem, no singular para as demasi operações)
async def get_user(pk: int):
    try:
        return users[pk]
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with pk {pk} not found'
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Internal Server Error'
        )
