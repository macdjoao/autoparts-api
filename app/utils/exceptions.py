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


def raise_email_already_registered_exception(email: str) -> HTTPException:
    email_already_registered_exception = HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f'Email {email} already registered',
    )
    raise email_already_registered_exception


def raise_incorrect_email_or_password_exception() -> HTTPException:
    incorrect_email_or_password_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        headers={'WWW-Authenticate': 'Bearer'}
    )
    raise incorrect_email_or_password_exception
