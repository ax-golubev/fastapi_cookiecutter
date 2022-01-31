#!/bin/sh

cmd="$@"

while ! nc -z -v $POSTGRES_HOST $POSTGRES_PORT;
do
  echo $POSTGRES_HOST
  >&2 echo "POSTGRESQL is unavailable - sleeping"
  sleep 2;
done

exec $cmd
