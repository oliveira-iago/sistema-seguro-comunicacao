import bcrypt, sqlite3, time, re, os

def pausa():
    time.sleep(1.5)
    input('\n> Pressione ENTER para voltar ao menu')

# Menu principal responsável por chamar as demais funções
def menu():
    global executar

    # Limpa a tela do terminal (windows ou linux)
    os.system('cls' if os.name == 'nt' else 'clear')

    print('''\n\n
    SISTEMA SEGURO DE COMUNICAÇÃO

        Digite a opção desejada

        1 - Realizar login
        2 - Registro de novo usuário
        3 - Consultar usuários registrados
        4 - Testar segurança de senhas com força bruta
        5 - Encerrar
    ''')

    opcao = str(input(' opção desejada: '))

    if opcao == '1':
        login()
    
    elif opcao == '2':
        registrarUsuario()
    
    elif opcao == '3':
        consultarUsuarios()

    elif opcao == '4':
        testarForcaBruta()

    elif opcao == '5':
        executar = False
    
    else:
        print('\nOPÇÃO INVÁLIDA!')

# Transforma string para bytes
def stringParaBytes(valor: str):
    return bytes(valor, 'utf-8')

# Transforma bytes para string
def bytesParaString(valor: bytes):
    return valor.decode('utf-8')

# Retorna o hash da senha
def criptografarSenha(senha: str, salt: str):
    return bcrypt.hashpw(senha.encode('utf-8'), salt).decode()

def login(tentativas: int=0):
    limite_tentativas = 5
    tentativas += 1
    
    if tentativas > limite_tentativas:
        print('\nNúmero de tentativas excedido! Aguarde 5 minutos para tentar novamente')
        time.sleep(300)
    
    else: 
        usuario = str(input('\nUsuário: ')).lower()
        senha = str(input('Senha: '))

        # Busca o salt do usuário no banco de dados
        cursor.execute(f"SELECT salt FROM {nome_tabela} WHERE username=?", (usuario,))
        linha = cursor.fetchone()

        if linha:
            salt = linha[0]
            senha_hashed = criptografarSenha(senha, stringParaBytes(salt))

            # Verifica se o hash da senha corresponde ao armazenado no banco de dados
            cursor.execute(f"SELECT id FROM {nome_tabela} WHERE username=? AND password_hash=?", (usuario, senha_hashed))
            linha_2 = cursor.fetchone()

            if linha_2:
                id = linha_2[0]
                print(f'\nLogin efetuado com sucesso! (id: {id})')

            else:
                print('\nSenha incorreta!. Tentativas restantes:', (limite_tentativas-tentativas))
                login(tentativas)

        else:
            print('\nUsuário não encontrado!')
            login(tentativas-1)


# Valida os requisitos minimos da senha
def validarForcaSenha(senha):
    # ao menos 6 dígitos
    if (len(senha) >= 6 and
        # ao menos uma letra maiúscula
        re.search(r'[A-Z]', senha) and
        # ao menos uma letra minúscula 
        re.search(r'[a-z]', senha) and
        # ao menos um número 
        re.search(r'[0-9]', senha) and
        # ao menos um caractere especial
        re.search(r'[\W_]', senha)):
        return True
    return False

# Salva as informações do usuário no banco de dados
def registrarUsuario():
    usuario = str(input('\nUsuário: ')).lower()
    senha = str(input('Senha: '))

    if not validarForcaSenha(senha):
        print('\nSenha fraca! A senha deve conter ao menos:')
        print('- 6 dígitos')
        print('- uma letra maiúscula')
        print('- uma letra minúscula')
        print('- um número')
        print('- um caractere especial')
        registrarUsuario()
    else:
        salt = bcrypt.gensalt()
        senha_hashed = criptografarSenha(senha, salt)

        try:
            cursor.execute(f"INSERT INTO {nome_tabela} (username, password_hash, salt) VALUES(?, ?, ?)", (usuario, senha_hashed, bytesParaString(salt)))
            conn.commit()
            print('\nUsuário registrado com sucesso!')
            pausa()

        except sqlite3.IntegrityError as e:
            # Erro é devido a um username já existente
            if 'UNIQUE constraint failed' in str(e):
                print('\n\nErro: O username já existe. Tente outro username.\n')
            else:
                print('\n\nErro de integridade ao registrar usuário. Tente novamente.\n')
                print(e)
            
            registrarUsuario()

        except Exception as e:
            print('\n\nErro ao registrar usuário. Tente novamente.\n')
            print(e)
            registrarUsuario()


# Exibe as informações dos usuários cadastrados no banco de dados
def consultarUsuarios():
    print('\n\nUsuários registrados\n')
    # Cabeçalhos das colunas
    print(f'{"ID":<5} {"Username":<20} {"Password Hash":<60} {"Salt":<60}')
    print('-' * 145)

    # Corpo da tabela
    for linha in cursor.execute(f'SELECT * FROM {nome_tabela}'):
        id, username, password_hash, salt = linha
        print(f'{id:<5} {username:<20} {password_hash:<60} {salt:<60}')
    
    pausa()

def testarForcaBruta():
    # Lista de senhas comuns para tentativa de força bruta
    senhas_comuns = ['1234', '12345', '123456', '1234567', '123456789', '1234567890', 'password', 'senha', 'abc123', 'password1', 'senha1']

    # Busca todos os usuários e suas senhas hash no banco de dados
    cursor.execute(f"SELECT username, password_hash, salt FROM {nome_tabela}")
    usuarios = cursor.fetchall()

    for usuario in usuarios:
        username, password_hash, salt = usuario
        salt = stringParaBytes(salt)
        print(f'\nTentando quebrar a senha do usuário: {username}')

        for senha in senhas_comuns:
            # Gera o hash da senha tentativa
            senha_hashed = criptografarSenha(senha, salt)

            # Verifica se o hash gerado corresponde ao armazenado no banco de dados
            if senha_hashed == password_hash:
                print(f'Senha encontrada para o usuário {username}: {senha}')
                break
        else:
            print(f'Não foi possível quebrar a senha do usuário {username} com a lista de senhas comuns.')

    pausa()

nome_tabela = 'usuarios'
# Conexão com banco de dados
conn = sqlite3.connect('users.db')

# Criação do cursor para comandos SQL
cursor = conn.cursor()

# Deleta a tabela caso exista
# cursor.execute(f'DROP TABLE IF EXISTS {nome_tabela}')

# Cria a tabela usuários no banco de dados
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

# Encerra o cursor e a conexão com o banco de dados
cursor.close()
conn.close()