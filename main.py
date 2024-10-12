import uuid

from fastapi import FastAPI

from constants import run_settings

app = FastAPI()

users = {
    1: {
        'id': str(uuid.uuid4()),
        'email': 'arthur@email.com',
        'first_name': 'arthur',
        'last_nanme': 'morgan',
        'password': 'pw',
        'role': 'admin'
    },
    2: {
        'id': str(uuid.uuid4()),
        'email': 'john@email.com',
        'first_name': 'john',
        'last_nanme': 'marston',
        'password': 'pw',
        'role': 'staff'
    },
    3: {
        'id': str(uuid.uuid4()),
        'email': 'jack@email.com',
        'first_name': 'jack',
        'last_nanme': 'marston',
        'password': 'pw',
        'role': 'staff'
    },
}


@app.get('/ping')
def ping():
    return {'detail': 'pong'}


@app.get('/users')
def get_users():
    return users


@app.get('/users/{id}')
def get_user(id: int):
    return users[id]


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        # TODO descobrir porque quando " reload=True ", não se pode usar " app=app ", sendo necessário o uso de " app='main:app' ".
        app='main:app',
        host=run_settings.get('HOST'),
        port=run_settings.get('PORT'),
        reload=run_settings.get('RELOAD')
    )
