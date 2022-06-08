python3 -m venv ../venv/
source ../venv/bin/activate
pip install Django==2.2.27
pip install psycopg2-binary==2.8.6
pip install pandas==1.4.1
docker pull postgres
docker build -t ikp-0 .
docker run -d --name ikp-0-container -p 5432:5432 ikp-0
docker start ikp-0-container
python ../populate_db.py
python ../IKP_app/manage.py runserver