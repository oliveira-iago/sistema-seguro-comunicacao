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
