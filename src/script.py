import bcrypt, sqlite3, time

def pausa():
    time.sleep(1.5)
    input('\n> Pressione ENTER para voltar ao menu')

#Menu principal responsável por chamar as demais funções
def menu():
    global executar

    print('''\n\n
    SISTEMA SEGURO DE COMUNICAÇÃO

        Digite a opção desejada

        1 - Realizar login
        2 - Registro de novo usuário
        3 - Consultar usuários registrados
        4 - Encerrar
    ''')

    opcao = str(input(' opção desejada: '))

    if opcao == '1':
        login()
    
    elif opcao == '2':
        registrarUsuario()
    
    elif opcao == '3':
        consultarUsuarios()

    elif opcao == '4':
        executar = False
    
    else:
        print('\nOPÇÃO INVÁLIDA!')


#Transforma string para bytes
def stringParaBytes(valor: str):
    return bytes(valor, 'utf-8')


#Transforma bytes para string
def bytesParaString(valor: bytes):
    return valor.decode('utf-8')


#Retorna o hash da senha
def criptografarSenha(senha: str, salt: str):
    return bcrypt.hashpw(senha.encode('utf-8'), salt).decode()


def login():
    usuario = str(input('\nusuario: ')).lower()
    senha = str(input('senha: '))

    cursor.execute(f"SELECT salt FROM {nome_tabela} WHERE username='{usuario}'")
    linhas = cursor.fetchall()

    if len(linhas):
        for linha in linhas:
            salt = linha[0]
            senha_hashed = criptografarSenha(senha, stringParaBytes(salt))

            cursor.execute(f"SELECT id FROM {nome_tabela} WHERE username='{usuario}' AND password_hash='{senha_hashed}'")
            linhas_2 = cursor.fetchall()

            if len(linhas_2):
                for linha_2 in linhas_2:
                    id = linha_2[0]
                    print(f'Login efetuado com sucesso! (id: {id})')
            else:
                print('\nSenha incorreta!')

    else:
        print('\nUsuário não encontrado!')

    time.sleep(1.5)


#Salva as informações do usuário no banco de dados
def registrarUsuario():
    usuario = str(input('\nusuario: ')).lower()
    senha = str(input('senha: '))

    salt = bcrypt.gensalt()
    senha_hashed = criptografarSenha(senha, salt)

    try:
        cursor.execute(f"""
            INSERT INTO {nome_tabela} (username, password_hash, salt)
            VALUES('{usuario}', '{senha_hashed}', '{bytesParaString(salt)}')
        """)
        conn.commit()
        print('\nUsuário registrado com sucesso!')

    except Exception as error:
        print('\n\nErro ao registrar usuário. Tente mudar o username\n')
        print(error)

    pausa()


#Exibe as informações dos usuários cadastrados no banco de dados
def consultarUsuarios():
    #Retorna o conteudo da tabela usuarios
    for linha in cursor.execute(f'SELECT * FROM {nome_tabela}'):
        print(linha)
    
    pausa()


nome_tabela = 'usuarios'
#Conexão com banco de dados
conn = sqlite3.connect('users.db')

#Criação do cursor para comandos sql
cursor = conn.cursor()

#Deleta a tabela caso exista
# cursor.execute(f'DROP TABLE IF EXISTS {nome_tabela}')

#Cria a tabela usuários no banco de dados
cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {nome_tabela} (
        id INTEGER PRIMARY KEY, 
        username VARCHAR(20) NOT NULL,
        password_hash VARCHAR(300) NOT NULL,
        salt VARCHAR(300) NOT NULL,
        CONSTRAINT valor_unico UNIQUE (username)
    )
''')
conn.commit()

executar = True
while executar:
    menu()


#Encerra o cursor e a conexão com o banco de dados
cursor.close()
conn.close()