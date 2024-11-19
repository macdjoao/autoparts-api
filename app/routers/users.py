from uuid import UUID

from fastapi import APIRouter, HTTPException, status, Depends
# from fastapi import Path, Query, Header       TODO: Fazer alguns testes com essas funções - https://sqlmodel.tiangolo.com/tutorial/fastapi/limit-and-offset/
from sqlmodel import Session, select

from app.utils.dependencies import get_session
from app.utils.security import get_current_active_user, get_password_hash
from app.models.users import User, UserCreate, UserFilter, UserPublic, UserUpdate, UserPartialUpdate
from app.utils.exceptions import raise_email_already_registered_exception, raise_internal_server_error_exception, raise_pk_not_found_exception


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
    summary='Lista usuários',  # A documentação Swagger será escrita em português
    description='Lista todos os usuários cadastrados no sistema'
)
# Padrão de nomenclatura das funções de endpoint: verbo http + recurso (no plural para listagem, no singular para as demasi operações)
async def get_users(
    current_user: User = Depends(get_current_active_user),
    filters: UserFilter = Depends(),
    session: Session = Depends(get_session)
):
    try:
        # status_code padrão é 200, estou explicitando só para frisar a existência do parâmetro
        query = select(User)
        if filters.pk:
            query = query.where(User.pk == filters.pk)
        if filters.email:
            query = query.where(User.email.contains(filters.email))
        if filters.first_name:
            query = query.where(User.first_name.contains(filters.first_name))
        if filters.last_name:
            query = query.where(User.last_name.contains(filters.last_name))
        if filters.is_active is not None:
            query = query.where(User.is_active == filters.is_active)
        db_users = session.exec(query).all()
        return db_users
    except Exception:
        raise_internal_server_error_exception()


@router.get(
    '/{pk}',
    response_model=UserPublic,
    status_code=status.HTTP_200_OK,
    summary='Busca usuário',
    description='Busca um usuário cadastrado no sistema, baseado em sua chave primária'
)
async def get_user(
    pk: UUID,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    try:
        db_user = session.get(User, pk)
        if db_user:
            return db_user
        raise_pk_not_found_exception(pk=pk)
    except HTTPException as exc:
        raise exc
    except Exception:
        raise_internal_server_error_exception()


@router.post(
    '',
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
    summary='Cadastra usuário',
    description='Cadastra um novo usuário no sistema.'
)
async def post_user(
    user: UserCreate,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    try:
        email_already_registered = session.exec(
            select(User).where(User.email == user.email)).first()
        if email_already_registered:
            raise raise_email_already_registered_exception(email=user.email)
        hashed_password = get_password_hash(user.password)
        extra_data = {'hashed_password': hashed_password}
        db_user = User.model_validate(user, update=extra_data)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
    except HTTPException as exc:
        raise exc
    except Exception as exc:
        raise_internal_server_error_exception()


@router.put(
    '/{pk}',
    response_model=UserPublic,
    summary='Atualiza usuário',
    description='Atualiza um usuário previamente cadastrado no sistema.'
)  # PUT deve receber em seu request todos os campos que podem ser alterados (exceto senha), diferente do PATCH, que é usado para atualizações parciais
async def put_user(
    pk: UUID,
    user: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    try:

        db_user = session.get(User, pk)
        if not db_user:
            raise_pk_not_found_exception(pk=pk)

        email_already_registered = session.exec(
            select(User).where(User.email == user.email, User.pk != pk)
        ).first()
        if email_already_registered:
            raise raise_email_already_registered_exception(
                email=user.email)

        user_data = user.model_dump()

        db_user.sqlmodel_update(user_data)

        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        return db_user

    except HTTPException as exc:
        raise exc
    except Exception:
        raise_internal_server_error_exception()


@router.patch(
    '/{pk}',
    response_model=UserPublic,
    status_code=status.HTTP_202_ACCEPTED,
    summary='Atualiza parcialmente um usuário',
    description='Atualiza parcialmente um usuário previamente cadastrado no sistema.'
)
async def patch_user(
    pk: UUID,
    user: UserPartialUpdate,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    # Caso o client queira atualizar o valor de algum campo para None, deve passar no request {"key": null}
    # Se a chave não for informada, o valor não é alterado
    # https://sqlmodel.tiangolo.com/tutorial/fastapi/update/#update-the-hero-in-the-database
    try:

        db_user = session.get(User, pk)
        if not db_user:
            raise_pk_not_found_exception(pk=pk)

        if user.email:
            email_already_registered = session.exec(
                select(User).where(User.email == user.email, User.pk != pk)
            ).first()
            if email_already_registered:
                raise raise_email_already_registered_exception(
                    email=user.email)

        user_data = user.model_dump(exclude_unset=True)
        extra_data = {}

        if 'password' in user_data:
            extra_data['hashed_password'] = get_password_hash(
                user_data.pop('password')
            )

        db_user.sqlmodel_update(user_data, update=extra_data)

        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        # Se a transação der certo, o FastAPI automaticamente retorna o status_code especificado no decorator
        # Se a transação der certo, o FastAPI automaticamente instancia o retorno no response_model especificado no decorator
        return db_user

    except HTTPException as exc:
        raise exc
    except Exception:
        raise_internal_server_error_exception()


@router.delete(
    '/{pk}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Deleta usuário',
    description='Deleta um usuário previamente cadastrado no sistema.'
)
async def delete_user(
    pk: UUID,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    try:
        db_user = session.get(User, pk)
        if db_user:
            session.delete(db_user)
            session.commit()
            return  # O retorno de um endpoint de verbo DELETE deve ser apenas o status code
        raise_pk_not_found_exception(pk=pk)
    except HTTPException as exc:
        raise exc
    except Exception:
        raise_internal_server_error_exception()
