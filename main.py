from typing import List
import uuid

from fastapi import FastAPI, HTTPException, status

from constants import run_settings
from schemas import User

app = FastAPI(
    title='AutoParts API',
    summary='Sistema de gerenciamento de estoque de autopeças',
    version='0.0.1'
)

# Nomearei o identificador com "pk", para evitar possíveis problemas, pois "id" é um palavra reservada do Python.
# Usarei "uuid" como chave primária, em vez de "int auto increment", esse valor deve ser gerado pelo BD.
# Ao usar uuid, perdemos peformance (um select realizado em uma coluna do tipo integer é mais rápido do que em uma coluna do tipo string/uuid);
# Tambem perdemos um pouco de armazenamento, já que uma string/uuid precisa de mais espaço para armazenamento do que um integer;
# No entanto, ganhamos em segurança, uma vez que dados como o número de registros de uma tabela não será facilmente identificado por agentes maliciosos.
users = {
    1: {
        'pk': str(uuid.uuid4()),
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
@app.get(
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


@app.get(
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


# Adicionando esse trecho de código ao fim do arquivo main, ao chamar "$ python3 main.py",
# temos o mesmo efeito que "$ uvicorn main:app --port 8081 --reload".
# Outra forma de executar a aplicação, pelo menos em ambiente de dev, é usando "$ fastapi dev main.py"
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        # Em vez de passar 'main:app', pode-se passar a variável app.
        # Mas quando passamos o parâmetro reload, é necessário que seja a string 'main:app'
        app='main:app',
        host=run_settings.get('HOST'),
        port=run_settings.get('PORT'),
        reload=run_settings.get('RELOAD')
    )
