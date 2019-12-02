start:
	python manage.py migrate
	python manage.py runserver
	echo Please visit: localhost:8080/museum
	echo Admin url: localhost:8080/museum/admin

admin:
	python manage.py createsuperuser
