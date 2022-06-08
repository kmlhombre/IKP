FROM ubuntu:latest
RUN apt-get -y update
RUN apt-get -y install git
RUN git clone https://github.com/kmlhombre/IKP.git
RUN cd IKP
FROM postgres:latest
ENV POSTGRES_PASSWORD=admin
ENV POSTGRES_USER=postgres
ENV POSTGRES_DB=ikp_hcp
RUN psql -U postgres postgres -f create_table.sql
RUN psql -U postgres postgres -f populate_database_with_examples.sql
