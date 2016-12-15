build:
	docker build -t cleaner .
tag:
	docker tag cleaner:latest bernardovale/docker_cleaner
push:
	docker push bernardovale/docker_cleaner
deploy: tag push

test:
	docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock cleaner
