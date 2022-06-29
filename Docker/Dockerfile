FROM postgres:latest
ENV POSTGRES_PASSWORD=admin
ENV POSTGRES_USER=postgres
ENV POSTGRES_DB=ikp_hcp
COPY IKP/Docker/create_db.sql /docker-entrypoint-initdb.d/init.sql