#!/bin/bash
coverage run --source='.' manage.py test --debug-mode --debug-sql

coverage report -m --skip-empty