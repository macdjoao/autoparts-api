from fastapi import FastAPI

from constants import run_settings

app = FastAPI()


@app.get('/ping')
def ping():
    return {'detail': 'pong'}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        # TODO descobrir porque quando " reload=True ", não se pode usar " app=app ", sendo necessário o uso de " app='main:app' ".
        app='main:app',
        host=run_settings.get('HOST'),
        port=run_settings.get('PORT'),
        reload=run_settings.get('RELOAD')
    )
