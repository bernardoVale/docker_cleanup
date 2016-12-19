.PHONY: build tag push deploy test env

build:
	docker build -t cleaner .
tag:
	docker tag cleaner:latest bernardovale/docker_cleanup
push:
	@echo "If you got erros execute first `docker login`"
	docker push bernardovale/docker_cleaner

deploy: tag push

test:
	docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock \
	-e WAKEUP_TIME=60 \
	-e KEEP_AMOUNT=10 \
	-e DELETE_IMAGES=nginx,mysql \
 	cleaner 
env:
	virtualenv env
	@echo "\n\nNow execute:   source env/bin/activate"