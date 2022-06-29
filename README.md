# IKP

Python 3.9.9 \
Django==2.2.27 \
psycopg2==2.8.6 \ 
pandas==1.4.1

# Creating and populate database
1. Run code from create_table.sql
2. Run code from populate_database_with_examples.sql
3. Run script populate_db.py

# How to use app on Linux
Requirements:
docker-ce docker-ce-cli containerd.io docker-compose-plugin

1. git clone https://github.com/kmlhombre/IKP
2. cd IKP
3. chmod 777 Docker/run.sh
4. ./run.sh
5. 