# Library API

simple api to borrow and return books in fastapi

### Installation
1. Make sure you have [poetry](https://python-poetry.org/) is installed in your system.
2. Execute the following command. This will create a virtual environment and install the packages.
```bash
poetry install
```

### Run migrations
1. Make sure proper environment variables are set. Check out .env-example for the list of all the environment variables.
2. Execute the following command. This will apply the database migrations.
```bash
alembic upgrade head
```

### Starting the development server
1. To run the server execute the following command.
```bash
fastapi dev main.py
```
2. By default the server runs at http://localhost:8000
3. open http://localhost:8000/docs for swagger documentation