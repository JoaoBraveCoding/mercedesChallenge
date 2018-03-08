# To run this script execute the following command in the root dir of
# the project: chmod 755 run.sh

python3.6 manage.py makemigrations
python3.6 manage.py migrate
python3.6 manage.py runscript script
python3.6 manage.py runserver