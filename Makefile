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
# Initial website performance check.
check:
	curl -X GET  http://127.0.0.1
exec:
	docker exec -it web_app bash