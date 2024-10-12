from fastapi import FastAPI


app = FastAPI()


@app.get('/ping')
def ping():
    return {'detail': 'pong'}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app=app)
