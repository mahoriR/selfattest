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

CREATE DATABASE esm_platform;
CREATE USER esm_platform_user WITH PASSWORD 'esm_platform_user_pwd';
ALTER ROLE esm_platform_user SET client_encoding TO 'utf8';
ALTER ROLE esm_platform_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE esm_platform_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE esm_platform TO esm_platform_user;

ALTER ROLE  esm_platform_user CREATEDB ; #Required only for running Unit tests locally.
\q

```

The DB connection string is  `postgres://esm_platform_user:esm_platform_user_pwd@localhost:5433/esm_platform`

Udpdate your .env file's `DATABASE_URL`

Connect to DB from command line using psql -

```bash
psql -d postgres://esm_platform_user:esm_platform_user_pwd@localhost:5433/esm_platform
```

### Running Tests

```bash
./run_tests.sh
```

### Running locally

```bash
python manage.py runserver
```

This shall run your local server along with nice browsable APIs

# How to setup a new environment

## Set Domain on digital ocean

## Create load balancer

HTTPS 443 - > HTTP 80
HTTP 80 -> HTTP 80

Create ceritificate and use subdomains. Subdomain must be already defined in domain config.

## Create new firewall. Allow incoming in for droplet from loadbalancer only. SSH from everyone

## Create new droplet

Follow https://github.com/mahoriR/ubuntu-server-setup.git
