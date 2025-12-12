.PHONY: run

run:
	docker-compose --env-file=.env -f deploy/dockers/compose.yml up --build -d
