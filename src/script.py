# Iago Leonardo Alves de Oliveira
# RGM: 11242400738

import bcrypt, sqlite3, time, re, os, socket, random

def pausa():
    time.sleep(1.5)
    input('\n> Pressione ENTER para voltar ao menu')

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

# Menu principal responsável por chamar as demais funções
def menu():
    global executar

    limpar_tela()

    print('''\n
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║                 [SISTEMA SEGURO DE COMUNICAÇÃO]                  ║
    ║                                                                  ║
    ║        Digite o número da opção desejada                         ║
    ║                                                                  ║
    ║        [1] - Realizar login                                      ║
    ║        [2] - Registrar novo usuário                              ║
    ║        [3] - Consultar usuários registrados                      ║
    ║        [4] - Consultar logs de login                             ║
    ║        [5] - Testar segurança de senhas com força bruta          ║
    ║        [6] - Encerrar                                            ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    ''')

    opcao = str(input('Opção desejada: '))

    if opcao == '1':
        login()
    
    elif opcao == '2':
        registrarUsuario()
    
    elif opcao == '3':
        consultarUsuarios()

    elif opcao == '4':
        consultarLogsLogin()

    elif opcao == '5':
        testarForcaBruta()

    elif opcao == '6':
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

# Salva um registro para cada tentativa de login
def registrarLogLogin(usuario, sucesso):
    ip = socket.gethostbyname(socket.gethostname())
    cursor.execute(f"INSERT INTO logs (username, sucesso, ip) VALUES (?, ?, ?)", (usuario, sucesso, ip))
    conn.commit()

def obterSaltUsuario(usuario):
    cursor.execute(f"SELECT salt FROM usuarios WHERE username=?", (usuario,))
    return cursor.fetchone()

# Simula enviar um código de verificação via SMS
def enviarCodigoVerificacao():
    # Gera um código aleatório de 6 dígitos
    codigo = random.randint(100000, 999999)
    return codigo

def login(tentativas: int=0):
    print(f'''\n
                ╔════════════════════════════════╗
                ║                                ║
                ║        REALIZAR LOGIN          ║
                ║                                ║
                ╚════════════════════════════════╝
                ''')
    
    limite_tentativas = 5
    tentativas += 1
    
    if tentativas > limite_tentativas:
        print('\nNúmero de tentativas excedido! Aguarde 5 minutos para tentar novamente')
        time.sleep(300)
    
    else: 
        usuario = str(input('\nUsuário: ')).lower()
        senha = str(input('Senha: '))

        # Busca o salt do usuário no banco de dados
        salts = obterSaltUsuario(usuario)

        if salts:
            salt = salts[0]
            senha_hashed = criptografarSenha(senha, stringParaBytes(salt))

            # Verifica se o hash da senha corresponde ao armazenado no banco de dados
            cursor.execute(f"SELECT id FROM usuarios WHERE username=? AND password_hash=?", (usuario, senha_hashed))
            ids = cursor.fetchone()
            
            if ids:
                id = ids[0]
                codigo_enviado = enviarCodigoVerificacao()

                print(f'''\n
                ╔══════════════════════════════════════════════════════════════════╗
                ║                     (Apenas uma simulação)                       ║
                ║                                                                  ║
                ║                  AUTENTICAÇÃO DE DOIS FATORES                    ║
                ║                                                                  ║
                ║            Código de verificação enviado [{codigo_enviado}]                ║
                ║                                                                  ║
                ╚══════════════════════════════════════════════════════════════════╝
                ''')

                codigo_digitado = int(input('\nDigite o código de verificação recebido via SMS: '))

                if codigo_digitado == codigo_enviado:
                    print(f'''\n
                ╔═════════════════════════════════════════════╗
                ║                                             ║
                ║        LOGIN EFETUADO COM SUCESSO!          ║
                ║                                             ║
                ║           (ID DE USUÁRIO: {id})                ║
                ║                                             ║
                ╚═════════════════════════════════════════════╝
                ''')
                    registrarLogLogin(usuario, True)
                    pausa()
                else:
                    print('\nCódigo de verificação incorreto!')
                    registrarLogLogin(usuario, False)
                    login(tentativas)

            else:
                print('\nSenha incorreta!. Tentativas restantes:', (limite_tentativas-tentativas))
                registrarLogLogin(usuario, False)
                login(tentativas)

        else:
            print('\nUsuário não encontrado!')
            registrarLogLogin(usuario, False)
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
    print(f'''\n
                ╔══════════════════════════════════════════╗
                ║                                          ║
                ║        REGISTRO DE NOVO USUÁRIO          ║
                ║                                          ║
                ╚══════════════════════════════════════════╝
                ''')
    
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
            cursor.execute(f"INSERT INTO usuarios (username, password_hash, salt) VALUES(?, ?, ?)", (usuario, senha_hashed, bytesParaString(salt)))
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
    print(f'''\n
                ╔══════════════════════════════════════════════════╗
                ║                                                  ║
                ║        CONSULTA DE USUÁRIOS REGISTRADOS          ║
                ║                                                  ║
                ╚══════════════════════════════════════════════════╝
                ''')
    # Cabeçalhos das colunas
    print(f'{"ID":<5} {"Username":<20} {"Password Hash":<60} {"Salt":<60}')
    print('-' * 145)

    # Corpo da tabela
    for linha in cursor.execute(f'SELECT * FROM usuarios'):
        id, username, password_hash, salt = linha
        print(f'{id:<5} {username:<20} {password_hash:<60} {salt:<60}')
    
    pausa()

# Exibe os logs de login no banco de dados
def consultarLogsLogin():
    print(f'''\n
                ╔═══════════════════════════════════════════╗
                ║                                           ║
                ║        CONSULTA DE LOGS DE LOGINS         ║
                ║                                           ║
                ╚═══════════════════════════════════════════╝
                ''')
    # Cabeçalhos das colunas
    print(f'{"ID":<5} {"Username":<20} {"IP":<15} {"Sucesso":<10} {"Timestamp":<20}')
    print('-' * 145)

    # Corpo da tabela
    for linha in cursor.execute('SELECT * FROM logs'):
        id, username, ip, sucesso, timestamp = linha
        print(f'{id:<5} {username:<20} {ip:<15} {sucesso:<10} {timestamp:<20}')
    
    pausa()

def testarForcaBruta():
    print(f'''\n
                ╔══════════════════════════════════════╗
                ║                                      ║
                ║        TESTES DE FORÇA BRUTA         ║
                ║                                      ║
                ╚══════════════════════════════════════╝
                ''')
    # Lista de senhas comuns
    senhas_comuns = ['1234', '12345', '123456', '1234567', '12345678', '123456789', '1234567890', 'password', 'senha', 'abc123', 'password1', 'senha1']

    # Busca todos os usuários e suas senhas hash no banco de dados
    cursor.execute(f"SELECT username, password_hash, salt FROM usuarios")
    usuarios = cursor.fetchall()

    if usuarios:
        for usuario in usuarios:
            username, password_hash, salt = usuario
            salt = stringParaBytes(salt)
            print(f'\nTentando quebrar a senha do usuário {username}...')

            tempo_inicio = time.time()

            for senha in senhas_comuns:
                # Gera o hash da senha tentativa
                senha_hashed = criptografarSenha(senha, salt)

                # Verifica se o hash gerado corresponde ao armazenado no banco de dados
                if senha_hashed == password_hash:
                    tempo_fim = time.time()
                    diferenca_tempo = tempo_fim - tempo_inicio
                    print(f'Senha encontrada para o usuário {username}: {senha}')
                    print(f'Tempo para quebrar a senha: {diferenca_tempo:.2f} segundos')
                    break
            else:
                print(f'Não foi possível quebrar a senha do usuário {username} com a lista de senhas comuns.')
    else:
        print('\nNão há usuários registrados no banco de dados.')

    pausa()


# Obtém o caminho atual de execução do script
caminho_atual = os.path.dirname(os.path.abspath(__file__))

# Conexão com banco de dados
conn = sqlite3.connect(os.path.join(caminho_atual, 'users.db'))

# Criação do cursor para comandos SQL
cursor = conn.cursor()

# Deleta a tabela caso exista
# cursor.execute(f'DROP TABLE IF EXISTS usuarios')

# Cria a tabela usuários no banco de dados
cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY, 
        username VARCHAR(20) NOT NULL,
        password_hash VARCHAR(300) NOT NULL,
        salt VARCHAR(300) NOT NULL,
        CONSTRAINT valor_unico UNIQUE (username)
    )
''')
conn.commit()

# Deleta a tabela caso exista
# cursor.execute(f'DROP TABLE IF EXISTS logs')

# Cria a tabela logs no banco de dados
cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY,
        username VARCHAR(20) NOT NULL,
        ip VARCHAR(45) NOT NULL,
        sucesso BOOLEAN NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()

executar = True
while executar:
    menu()

# Encerra o cursor e a conexão com o banco de dados
cursor.close()
conn.close()