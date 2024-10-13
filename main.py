from fastapi import FastAPI

from constants import run_settings
from routes import users

app = FastAPI(
    title='AutoParts API',
    summary='Sistema de gerenciamento de estoque de autopeças',
    version='0.0.1'
)

app.include_router(users.router)

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
