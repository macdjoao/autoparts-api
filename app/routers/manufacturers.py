from typing import Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status, Depends
from sqlmodel import Session, select

from app.models.manufacturers import ManufacturerPublic, Manufacturer, ManufacturerCreate
from app.models.users import User
from app.utils.dependencies import get_session
from app.utils.exceptions import raise_internal_server_error_exception, raise_name_already_registered_exception
from app.security.auth import get_current_active_user


router = APIRouter(
    prefix='/manufacturers',
    tags=['Manufacturers']
)


@router.get(
    '',
    response_model=list[ManufacturerPublic],
    summary='Lista fabricantes',
    description='Lista todas as fabricantes cadastradas no sistema'
)
async def get_manufacturers(
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
    pk: Optional[UUID] = Query(None, description='Chave primária'),
    name: Optional[str] = Query(None, description='Nome'),
    is_active: Optional[bool] = Query(True, description='Ativo')
):
    try:
        query = select(Manufacturer)
        if pk:
            query = query.where(Manufacturer.pk == pk)
        if name:
            query = query.where(Manufacturer.name.contains(name.capitalize()))
        if is_active is not None:
            query = query.where(Manufacturer.is_active == is_active)
        db_manufacturers = session.exec(query).all()
        return db_manufacturers
    except Exception:
        raise_internal_server_error_exception()


@router.post(
    '',
    response_model=ManufacturerPublic,
    status_code=status.HTTP_201_CREATED,
    summary='Cadastra fabricante',
    description='Cadastra uma nova fabricante no sistema.'
)
async def post_manufacturer(
    manufacturer: ManufacturerCreate,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    try:
        name_already_registered = session.exec(
            select(Manufacturer).where(Manufacturer.name == manufacturer.name)
        ).first()
        if name_already_registered:
            raise raise_name_already_registered_exception(
                name=manufacturer.name
            )
        extra_data = {
            'created_by': current_user.pk,
            'updated_by': current_user.pk,
        }
        db_manufacturer = Manufacturer.model_validate(
            manufacturer, update=extra_data
        )
        session.add(db_manufacturer)
        session.commit()
        session.refresh(db_manufacturer)
        return db_manufacturer
    except HTTPException as exc:
        raise exc
    except Exception as exc:
        raise_internal_server_error_exception()