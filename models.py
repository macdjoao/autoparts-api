import uuid

# Nomearei o identificador com "pk", para evitar possíveis problemas, pois "id" é um palavra reservada do Python.
# Usarei "uuid" como chave primária, em vez de "int auto increment", esse valor deve ser gerado pelo BD.
# Ao usar uuid, perdemos peformance (um select realizado em uma coluna do tipo integer é mais rápido do que em uma coluna do tipo string/uuid);
# Tambem perdemos um pouco de armazenamento, já que uma string/uuid precisa de mais espaço para armazenamento do que um integer;
# No entanto, ganhamos em segurança, uma vez que dados como o número de registros de uma tabela não será facilmente identificado por agentes maliciosos.
users = [
    {
        'pk': str(uuid.uuid4()),
        'email': 'arthur@email.com',
        'first_name': 'arthur',
        'last_name': 'morgan',
        'password': 'pw',
        'role': 'admin'
    },
    {
        'pk': str(uuid.uuid4()),
        'email': 'john@email.com',
        'first_name': 'john',
        'last_name': 'marston',
        'password': 'pw',
        'role': 'staff'
    },
    {
        'pk': str(uuid.uuid4()),
        'email': 'jack@email.com',
        'first_name': 'jack',
        'last_name': 'marston',
        'password': 'pw',
        'role': 'staff'
    }
]
