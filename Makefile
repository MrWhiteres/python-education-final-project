up:
	docker-compose up -d
down:
	docker-compose down
log:
	docker logs web_app
check:
	curl -X GET  http://127.0.0.1