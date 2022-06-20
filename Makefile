# Command starts docker container in silent mode without logs.
up:
	docker-compose --env-file .env up -d
# Command starts docker container in reconstruction mode.
build:
	docker-compose --env-file .env up --build
# Command disables all currently running docker containers.
down:
	docker-compose down
# Command prints the logs of the container with the flask application.
log:
	docker logs web_app
# The command allows you to use the terminal in a container with a web application
exec:
	docker exec -it web_app bash
# Must be used the first time the application is launched to add primary data. RUN only after starting the web container.
add:
	python project/database/db_add.py
# Add new Admin in site
admin:
	python project/database/db_add_admin.py
seed:
	python project/database/db_seed.py
test:
	pytest
rm:
	docker rm -f $(docker ps -a -q)