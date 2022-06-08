docker pull postgres
docker run --name postgres-ikp -e POSTGRES_PASSWORD="admin" POSTGRES_NAME="ikp_hcp" POSTGRES_USER="postgres" -d -p 5432:5432 postgres
docker exec -it postgres-ikp bash
cd ~
psql -U postgres
