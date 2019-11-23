#!/usr/bin/env bash
function clean_up {
    # Perform program exit housekeeping
    KILL $PIDDOC
    KILL $PIDMIX
    KILL $PIDRUN
    exit
}

trap clean_up SIGHUP SIGINT SIGTERM
docker-compose up &  PIDDOC=$!
pipenv run python manage.py migrate
pipenv run python manage.py watch &  PIDWAT=$!
pipenv run python manage.py runserver &  PIDRUN=$!
wait $PIDDOC
wait $PIDMIX
wait $PIDRUN