#!/bin/bash

git pull

docker-compose -f docker-compose-prod.yml build
docker-compose -f docker-compose-prod.yml up -d

docker-compose -f docker-compose-prod.yml exec web_monolith python manage.py migrate
