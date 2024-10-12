# autoparts-api
Sistema para gerenciar estoque de autopeças

## main.py
Para executar a aplicação, existem algumas possibilidades:

###### 1
Executando em um terminal, no diretório raiz do projeto:
```bash
$ uvicorn main:app
```
```main``` é o nome do arquivo onde está a instância de FastAPI, e ```app``` é o nome da variável que guarda a instância. Esse comando aceita parâmetros, por exemplo:
```$ uvicorn main:app --port 8081 --reload```, entre outros.

###### 2
Executando em um terminal, no diretório raiz do projeto:
```bash
$ fastapi dev main.py
```
Usando o CLI do FastAPI, executando o servidor em modo de desenvolvimento.

###### 3
Adicionando ao fim do arquivo main.py o trecho de código:
```python
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app=app)
```
Dessa forma, apenas utilizando ```$ python3 main.py```. ```uvicorn.run()``` tambem aceita os mesmos parâmetros que o a primeira forma de execução citada.