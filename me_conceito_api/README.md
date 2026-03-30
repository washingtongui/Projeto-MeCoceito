# me_conceito_api

Backend Django separado para o projeto Me Conceito.

## Como usar

1. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Ajuste o banco de dados se necessário.
   - Por padrão o projeto usa SQLite (`db.sqlite3`).
   - Para trocar de banco, defina variáveis de ambiente antes de rodar as migrações.

   Exemplo usando SQLite (padrão):
   ```bash
   set DJANGO_DB_ENGINE=django.db.backends.sqlite3
   set DJANGO_DB_NAME=db.sqlite3
   ```

   Exemplo usando PostgreSQL:
   ```bash
   set DJANGO_DB_ENGINE=django.db.backends.postgresql
   set DJANGO_DB_NAME=me_conceito_api
   set DJANGO_DB_USER=me_conceito_user
   set DJANGO_DB_PASSWORD=supersecret
   set DJANGO_DB_HOST=localhost
   set DJANGO_DB_PORT=5432
   ```

4. Execute as migrações:
   ```bash
   python manage.py migrate
   ```

5. Inicie o servidor:
   ```bash
   python manage.py runserver
   ```

O backend ficará disponível em `http://127.0.0.1:8000/` e a API em `http://127.0.0.1:8000/api/`.
