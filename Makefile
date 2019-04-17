.PHONY=dev
.DEFAULT_GOAL=dev


env:
	virtualenv3 env

dev: env
	source env/bin/activate && pip install -r requirements.txt
	source env/bin/activate && pip install -r requirements-dev.txt

runserver:
	./manage runserver
