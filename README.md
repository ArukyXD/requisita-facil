# Requisita Fácil — versão profissional

Sistema web para requisição de materiais de linha de produção.

## Stack

- Python + Flask
- SQLAlchemy ORM
- Flask-Login
- PostgreSQL em produção
- SQLite opcional em desenvolvimento
- Gunicorn
- Docker

## Recursos

- Login seguro com senha criptografada
- Perfis: operador, supervisor e almoxarifado
- Cadastro de materiais
- Criação de requisição
- Cálculo automático do material necessário
- Histórico
- Controle de status
- Layout responsivo
- Pronto para deploy com Docker

## Rodar local sem Docker

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
flask --app run.py init-db
flask --app run.py run
```

Acesse:

```text
http://127.0.0.1:5000
```

## Rodar local com Docker

```bash
docker compose up --build
```

Acesse:

```text
http://127.0.0.1:5000
```

## Usuários iniciais

```text
admin / admin123
operador / operador123
almox / almox123
```

## Deploy rápido no Render

1. Crie um repositório no GitHub.
2. Suba todos os arquivos deste projeto.
3. No Render, crie um banco PostgreSQL.
4. Crie um Web Service usando o repositório.
5. Escolha Docker como ambiente.
6. Adicione as variáveis:

```text
SECRET_KEY=uma_chave_grande_e_aleatoria
DATABASE_URL=url_do_postgres_do_render
PORT=10000
```

7. Faça o deploy.

O Dockerfile já roda a criação inicial do banco e inicia o app com Gunicorn.
