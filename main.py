import uuid

from fastapi import FastAPI, HTTPException, status

from constants import run_settings
from schemas import User

app = FastAPI()

# Nomearei o identificador com "pk", para evitar possíveis problemas, pois "id" é um palavra reservada do Python.
users = {
    1: {
        'pk': str(uuid.uuid4()),  # Esse valor deve ser gerado pelo SGBD
        'email': 'arthur@email.com',
        'first_name': 'arthur',
        'last_name': 'morgan',
        'password': 'pw',
        'role': 'admin'
    },
    2: {
        'pk': str(uuid.uuid4()),
        'email': 'john@email.com',
        'first_name': 'john',
        'last_name': 'marston',
        'password': 'pw',
        'role': 'staff'
    },
    3: {
        'pk': str(uuid.uuid4()),
        'email': 'jack@email.com',
        'first_name': 'jack',
        'last_name': 'marston',
        'password': 'pw',
        'role': 'staff'
    },
}


# Padrão de nomenclatura dos endpoints: "/resources".
# "/" + nome do recurso (substantivo) em que a operação está sendo realizada, sem "/" no final.
# Tanto singular "/resource", quanto plural "/resources", são aceitos, mas é importante seguir o padrão escolhido para todos os endpoints.
@app.get('/users')
def get_users():
    try:
        return users
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Internal Server Error'
        )


@app.get('/users/{pk}')
def get_user(pk: int) -> User:
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


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        # TODO descobrir porque quando " reload=True ", não se pode usar " app=app ", sendo necessário o uso de " app='main:app' ".
        app='main:app',
        host=run_settings.get('HOST'),
        port=run_settings.get('PORT'),
        reload=run_settings.get('RELOAD')
    )
