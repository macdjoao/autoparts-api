from fastapi import HTTPException, status

# Para seguir a recomendação DRY, irei separar as exceptions em funções reutilizaveis


def raise_internal_server_error_exception() -> HTTPException:
    internal_server_error_exception = HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail='Internal server error'
    )
    raise internal_server_error_exception


def raise_pk_not_found_exception(pk: int) -> HTTPException:
    not_found_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'No record with pk {pk}',
    )
    raise not_found_exception
