from typing import List

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
# from fastapi import Path, Query, Header       TODO: Fazer alguns testes com essas funções

from schemas.users import User
from models import users


router = APIRouter(
    prefix='/users',
    tags=['Users']
)


# Padrão de nomenclatura dos endpoints: "/api/v1/resources". (O prefixo "/api/v1" é adicionado em router para diminuir repetição)
# "/" + nome do recurso (substantivo) em que a operação está sendo realizada, sem "/" no final.
# Tanto singular "/resource", quanto plural "/resources", são aceitos, mas é importante seguir o padrão escolhido para todos os endpoints.
@router.get(
    '',
    # Passar "-> List[User]" como retorno na assinatura da função teria o mesmo efeito que response_model
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary='Lista usuários',
    description='Lista todos os usuários cadastrados no sistema'
)
# Padrão de nomenclatura das funções de endpoint: verbo http + recurso (no plural para listagem, no singular para as demasi operações)
async def get_users():
    try:
        # status_code padrão é 200, estou explicitando só para frisar a existência do parâmetro
        return JSONResponse(content=jsonable_encoder(users), status_code=status.HTTP_200_OK)
    except Exception as exc:
        print(exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Internal Server Error'
        )


@router.get(
    '/{pk}',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Busca usuário',
    description='Busca um usuário cadastrado no sistema, baseado em sua chave primária'
)
async def get_user(pk: int):
    try:
        user = users[pk-1]
        response = User(**user).model_dump()
        return JSONResponse(content=response, status_code=status.HTTP_200_OK)
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with pk {pk} not found'
        )
    except Exception as exc:
        print(exc)
        print(type(exc))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Internal Server Error'
        )


@router.post(
    '',
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary='Cadastra usuário',
    description='Cadastra um novo usuário no sistema.'
)
async def post_user(user: User):
    try:
        users.append(user)
        response: User = users[-1]
        return JSONResponse(content=response.model_dump(), status_code=status.HTTP_201_CREATED)
    except Exception as exc:
        print(exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Internal Server Error'
        )
