# Projeto Sistema Seguro de Comunicação
### Participantes:
* Brenno de Sousa Lemos - 11222100597
* Bruna de Medeiros Santos - 11222101313
* Iaago Alves de Oliveira - 11242400738
* João Gabriel Gomes - 11222101048

### Objetivo do projeto
Segurança na comunicação entre funcionários.
### Tecnologias utilizadas
* <b>bcrypt</b> → Hashing seguro de senhas.
* <b>PyJWT</b> → Autenticação via Tokens JWT.
* <b>cryptography</b> → Implementação de AES e RSA.
### Fluxo básico do sistema
* Usuário faz cadastro (senha armazenada com bcrypt).
* Usuário faz login (autenticado via JWT).
* Usuário envia uma mensagem criptografada com AES.
* Apenas o destinatário correto pode descriptografar com sua chave RSA.
### Principais etapas de implementação, incluindo
* <b>Cadastro de usuário</b> → Hash de senha com bcrypt.
* <b>Login</b> → Geração e verificação de Token JWT.
* <b>Criptografia de mensagens</b> → Uso de AES (CBC).
* <b>Proteção da chave AES</b> → Uso de RSA para criptografar a chave antes de armazená-la.
### Descrição do que o sistema faz
* <b>Cadastro de usuário</b> → Protege a senha com bcrypt antes de armazenar.
* <b>Login</b> → Se a senha estiver correta, gera um Token JWT.
* <b>Enviar mensagem</b> → A mensagem é criptografada com AES antes de ser salva.
* <b>Receber mensagem</b> → O usuário descriptografa com RSA sua chave AES e acessa a mensagem.
