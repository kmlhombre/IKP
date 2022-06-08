docker pull postgres
docker build -t ikp-0 .
docker run -d --name ikp-0-container -p 5432:5432 ikp-0
docker start ikp-0