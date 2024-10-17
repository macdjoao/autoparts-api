from uuid import UUID

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
# from fastapi import Path, Query, Header       TODO: Fazer alguns testes com essas funções
from sqlmodel import Session, select

from settings.database import get_session
from models.users import User


router = APIRouter(
    prefix='/users',
    tags=['Users']
)


# Padrão de nomenclatura dos endpoints: "/api/v1/resources". (O prefixo "/api/v1" é adicionado em router para diminuir repetição)
# "/" + nome do recurso (substantivo) em que a operação está sendo realizada, sem "/" no final.
# Tanto singular "/resource", quanto plural "/resources", são aceitos, mas é importante seguir o padrão escolhido para todos os endpoints.
@router.get(
    '',
    # Passar "-> list[User]" como retorno na assinatura da função teria o mesmo efeito que response_model
    response_model=list[User],
    status_code=status.HTTP_200_OK,
    summary='Lista usuários',  # A documentação Swagger será escrita em português
    description='Lista todos os usuários cadastrados no sistema'
)
# Padrão de nomenclatura das funções de endpoint: verbo http + recurso (no plural para listagem, no singular para as demasi operações)
async def get_users(session: Session = Depends(get_session)):
    try:
        # status_code padrão é 200, estou explicitando só para frisar a existência do parâmetro
        query = session.exec(select(User)).all()
        return JSONResponse(content=jsonable_encoder(query), status_code=status.HTTP_200_OK)
    except Exception:
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
async def get_user(pk: UUID, session: Session = Depends(get_session)):
    try:
        query = session.exec(select(User).where(User.pk == pk)).first()
        if query:
            return JSONResponse(content=jsonable_encoder(query), status_code=status.HTTP_200_OK)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with pk {pk} not found'
        )
    except Exception:
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
async def post_user(user: User, session: Session = Depends(get_session)):
    try:
        session.add(user)
        session.commit()
        session.refresh(user)
        return JSONResponse(content=jsonable_encoder(user), status_code=status.HTTP_201_CREATED)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Internal Server Error'
        )
