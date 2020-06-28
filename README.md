# Setting up a new production server

Follow <https://github.com/mahoriR/ubuntu-server-setup.git>


# Setup Debug Environment

## With Docker

## Starting local server

```bash
docker-compose -f docker-compose-dev.yml build
docker-compose -f docker-compose-dev.yml up -d
```

This shall run your local server along with nice browsable APIs at __127.0.0.1:8000__

## Running Unit Tests

```bash
docker-compose -f docker-compose-dev.yml exec web_monolith /bin/bash run_tests.sh
```

## Running Migrations

This will always be required when setting up dev env for first time

```bash
docker-compose -f docker-compose-dev.yml exec web_monolith python manage.py migrate
```

## Stop local server

Note: Your DB will presist data across container restarts

```bash
docker-compose -f docker-compose-dev.yml  down
```

## Without Docker

> Not sure, if you need to setup with docker of without? If you need to use this, you will already know why_

### Start with setting virtual environment

```bash
virtualenv --python=python3 ~/.virtualenvs/selfattest

source ~/.virtualenvs/selfattest/bin/activate

pip install -r requirements.txt
```

### IDE setup

Make sure you are using Python 3.6.9

```bash
python --version
```

Install pep8 for Python formatter

### PostgreSQL setup for local DEV

```bash
sudo su - postgres

psql -p <port>

CREATE DATABASE selfattest;
CREATE USER selfattest_user WITH PASSWORD 'selfattest_user_pwd';
ALTER ROLE selfattest_user SET client_encoding TO 'utf8';
ALTER ROLE selfattest_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE selfattest_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE selfattest TO selfattest_user;

ALTER ROLE  selfattest_user CREATEDB ; #Required only for running Unit tests locally.
\q

```

The DB connection string is  `postgres://selfattest_user:selfattest_user_pwd@localhost:5433/selfattest`

Udpdate your .env file's `DATABASE_URL`

Connect to DB from command line using psql -

```bash
psql -d postgres://selfattest_user:selfattest_user_pwd@localhost:5433/selfattest
```

### Running Tests

```bash
./run_tests.sh
```

### Running locally

```bash
python manage.py runserver
```
