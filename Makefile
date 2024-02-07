.PHONY: first_build build up down clean pytest doc jupyter mlflow


first_build:
	git init
	dvc commit
	docker compose build
	git add .
	git commit -m "first commit"
	git branch -M main
	git remote add origin https://github.com/githubjacky/calibrate-google-trends.git
	git push -u origin main


build:
	docker compose build


up:
	docker compose up


down:
	docker compose down


clean:
	docker rmi --force 0jacky/calibrate-google-trends:latest


pytest:
	docker compose run --rm pytest


doc:
	docker compose run --rm doc


jupyter:
	docker compose run --rm --service-ports jupyter-lab
