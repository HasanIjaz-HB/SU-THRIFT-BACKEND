# SU-THRIFT-BACKEND
Backend built for E-commerce store using Django
! IF YOU ADD ANY PACKAGES RUN : pip freeze > requirements.txt !!

1.Create virtual env
python3 -m venv venv
source venv/bin/activate  (for macos)
venv\Scripts\activate     (for windows)

2.Run virtual env
source venv/bin/activate  (for macos)
venv\Scripts\activate     (for windows)

3.Install requirements
cd src
pip3 install -r requirements.txt

4.Make database settings & migrations
python manage.py makemigrations
python manage.py migrate

5.Start django server
python manage.py runserver
