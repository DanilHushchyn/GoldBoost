MANAGE = python manage.py
ccc:
	ls
run:
	$(MANAGE) runserver

m1:
	$(MANAGE) makemigrations

m2:
	$(MANAGE) migrate

superuser:
	$(MANAGE) createsuperuser

worker:
	celery -A config worker -l info

dumpdata:
	$(MANAGE) dumpdata  -e contenttypes -e auth.Permission > db.json

dock-build:
	sudo docker-compose -f docker-compose.yml build

dock-up:
	sudo docker-compose -f docker-compose.yml up

down:
	sudo docker compose down -v
prune:
	sudo docker  system prune -a

startapp:
	$(MANAGE) migrate --no-input
	$(MANAGE) loaddata db.json
	$(MANAGE) collectstatic --no-input
	gunicorn GoldBoost.wsgi:application --bind 0.0.0.0:8000

createapp_example:
	$(MANAGE) startapp website ./src/website/
