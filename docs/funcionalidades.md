### Descrição do que o sistema faz
* <b>Cadastro de usuário</b> → Protege a senha com bcrypt antes de armazenar.
* <b>Login</b> → Se a senha estiver correta, gera um Token JWT.
* <b>Enviar mensagem</b> → A mensagem é criptografada com AES antes de ser salva.
* <b>Receber mensagem</b> → O usuário descriptografa com RSA sua chave AES e acessa a mensagem.
