FROM postgres:14.5-alpine3.16

COPY postgresql.conf /etc/postgresql/postgresql.conf

COPY init_scripts/* /docker-entrypoint-initdb.d/
