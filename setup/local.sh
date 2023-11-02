psql -h localhost -U postgres -p 5432 -a -q -f /home/mahdi/Desktop/projects/site/site-django/setup/create_db.sql;
rm -r .venv/;
python3 -m venv .venv;
source .venv/bin/activate;
pip install -r requirments.txt;
python manage.py migrate;
python manage.py runserver