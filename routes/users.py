from uuid import UUID

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
# from fastapi import Path, Query, Header       TODO: Fazer alguns testes com essas funções
from sqlmodel import Session, select

from settings.database import get_session
from models.users import User, UserCreate, UserPublic, UserUpdate


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
    response_model=list[UserPublic],
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
    except Exception as exc:
        print(exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Internal Server Error'
        )


@router.get(
    '/{pk}',
    response_model=UserPublic,
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
    except HTTPException as exc:
        raise exc
    except Exception as exc:
        print(exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Internal Server Error'
        )


@router.post(
    '',
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
    summary='Cadastra usuário',
    description='Cadastra um novo usuário no sistema.'
)
async def post_user(user: UserCreate, session: Session = Depends(get_session)):
    try:
        db_user = User.model_validate(user)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return JSONResponse(content=jsonable_encoder(db_user), status_code=status.HTTP_201_CREATED)
    except Exception as exc:
        print(exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Internal Server Error'
        )


@router.patch(
    '/{pk}',
    response_model=UserPublic,
    status_code=status.HTTP_202_ACCEPTED,
    summary='Atualiza usuário',
    description='Atualiza um usuário previamente cadastrado no sistema.'
)
async def patch_user(pk: UUID, user: UserUpdate, session: Session = Depends(get_session)):
    # Caso o client queira atualizar o valor de algum campo para None, deve passar no request {"key": null}
    # Se a chave não for informada, o valor não é alterado
    # https://sqlmodel.tiangolo.com/tutorial/fastapi/update/#update-the-hero-in-the-database
    try:
        db_user = session.get(User, pk)
        if db_user:
            user_data = user.model_dump(exclude_unset=True)
            db_user.sqlmodel_update(user_data)
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            # Se a transação der certo, o FastAPI automaticamente retorna o status_code especificado no decorator
            # Se a transação der certo, o FastAPI automaticamente instancia o retorno no response_model especificado no decorator
            return db_user
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with pk {pk} not found'
        )
    except HTTPException as exc:
        raise exc
    except Exception as exc:
        print(exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Internal Server Error'
        )
