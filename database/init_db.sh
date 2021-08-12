#!/bin/bash

sleep 15
echo '[Postgres dbConfig] Creating tables.'
until psql postgres postgres -f ./create_tables.sql
do
  echo "[Postgres dbConfig] Creating tables failed. Waiting 10 seconds to retry."
  sleep 10
done
echo "[Postgres dbConfig] Tables created."

