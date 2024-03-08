#!/usr/bin/env bash
set -e

if [ -z ${POSTGRES_TEST_DB+x} ]; then
    echo "Variable POSTGRES_TEST_DB is not set";
    exit 1
fi

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE $POSTGRES_TEST_DB;
    GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_TEST_DB TO $POSTGRES_USER;
EOSQL
