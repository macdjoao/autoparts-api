from fastapi import FastAPI

from settings.settings import settings
from routes import router

app = FastAPI(
    title='AutoParts API',
    summary='Sistema de gerenciamento de estoque de autopeças',
    version=settings.APP_VERSION
)

app.include_router(router.router)

# Adicionando esse trecho de código ao fim do arquivo main, ao chamar "$ python3 main.py",
# temos o mesmo efeito que "$ uvicorn main:app --port 8000 --reload".
# Outra forma de executar a aplicação, pelo menos em ambiente de dev, é usando "$ fastapi dev main.py"
# UPDATE: A forma correta de executar um app FastAPI é "$ fastapi dev main.py" em ambiente de desenvolvimento, e "$ fastapi run main.py" em ambiente de produção.
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        # Em vez de passar 'main:app', pode-se passar a variável app.
        # Mas quando passamos o parâmetro reload, é necessário que seja a string 'main:app'
        app=settings.APP,
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.APP_RELOAD
    )
