#!/usr/bin/env bash
docker-compose up &  PIDDOC=$!
pipenv run python manage.py test
KILL $PIDDOC
