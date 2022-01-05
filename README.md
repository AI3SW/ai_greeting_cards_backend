# Flask App Template

Boilerplate code for a flask app to wrap around a Machine Learning Model.

## Simple How to Use

* Clone this repo
* Update repository remote:

```bash
$ git remote set-url origin <newurl>
```

* Create your own model by extending from `BaseModel` in [declarations.py](flask_app/model/declarations.py)
* update `init_model_store` function in [`model` package](flask_app/model/__init__.py)
* update endpoints in [views.py](flask_app/views.py)

## Create Environment using Conda

```bash
$ # create conda environment
$ conda env create --file environments/environment.yml
$ conda activate ai-greeting-cards-flask
```

## Instance Configuration

In [./instance/config.py](instance/config.py):

```python
DB_USERNAME = "postgres"
DB_PASSWORD = "PASSWORD"
DB_IP_ADDR = "<DB_IP_ADDR>"
DB_PORT = "5432"
DATABASE_NAME = "<DATABASE_NAME>"
SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_IP_ADDR}:{DB_PORT}/{DATABASE_NAME}"
REDIS_IP_ADDR = "localhost"
REDIS_PORT = "6379"
REDIS_URL = f"redis://{REDIS_IP_ADDR}:{REDIS_PORT}"
MAIL_USERNAME = "<MAIL_USERNAME>"
MAIL_PASSWORD = "<MAIL_PASSWORD>"
MAIL_DEFAULT_SENDER = "<MAIL_DEFAULT_SENDER>"
```

## Serve Flask App

### Using Flask Built-in Development Server

```bash
$ export FLASK_APP=flask_app FLASK_ENV=development
$ flask run --host=0.0.0.0 --port=5000
```

## Databasing

### Run PostgreSQL using Docker

```bash
$ # Running db wih volume mounted for staging purposes
$ POSTGRES_PASSWORD=<your postgres password>
$ docker run --rm -p 5432:5432 --name postgres \
    -v /data/ai_greeting_cards:/var/lib/postgresql/data \
    -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD -d postgres

$ # stop container
$ docker stop postgres
```

### Create Database, Tables and Stored Procedures

Using `psql`:

```bash
$ POSTGRES_PASSWORD=<your postgres password>
$ PGPASSWORD=$POSTGRES_PASSWORD psql -U postgres -h localhost -f scripts/database/create_db.sql
$ PGPASSWORD=$POSTGRES_PASSWORD psql -U postgres -h localhost -d ai_3_staging_greeting_cards -f scripts/database/create_tables.sql
$ PGPASSWORD=$POSTGRES_PASSWORD psql -U postgres -h localhost -d ai_3_greeting_cards -f scripts/database/create_tables.sql
```

### Seed Database

```bash
# seed database
$ POSTGRES_PASSWORD=<your postgres password>
$ PGPASSWORD=$POSTGRES_PASSWORD psql -U postgres -h localhost -d ai_3_staging_greeting_cards -f scripts/database/seed_db.sql
```
