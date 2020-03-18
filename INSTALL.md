pip3 install -r requirements.txt

python3 manage.py migrate

python3 -W "ignore" manage.py runserver 0.0.0.0:8080