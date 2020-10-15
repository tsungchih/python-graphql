DOCKER:=/usr/local/bin/docker
PWD:=$(shell pwd)
DOCKERFILE:=docker/Dockerfile
DOCKER_TAG:=fastapi-test
DOCKER_VER:=latest

.PHONY: build
build:
	@$(DOCKER) build -f $(DOCKERFILE) -t $(DOCKER_TAG):$(DOCKER_VER) $(PWD)

.PHONY: run
run:
	@$(DOCKER) run --name $(DOCKER_TAG) -d -p 10443:443 -p 8080:80 -v $(PWD)/src/app:/app/app -v $(PWD)/certs:/certs $(DOCKER_TAG):$(DOCKER_VER)

.PHONY: attach
login:
	@$(DOCKER) attach $(DOCKER_TAG)

.PHONY: logs
logs:
	@$(DOCKER) logs $(DOCKER_TAG)

.PHONY: reload
reload:
	@$(DOCKER) run --name $(DOCKER_TAG) -d -p 10443:443 -p 8080:80 -v $(PWD)/src/app:/app/app -v $(PWD)/certs:/certs $(DOCKER_TAG):$(DOCKER_VER) /start-reload.sh

.PHONY: stop
stop:
	@$(DOCKER) stop $(DOCKER_TAG) && \
	$(DOCKER) rm -v $(DOCKER_TAG)

.PHONY: clean
clean:
	@$(DOCKER) rmi $(DOCKER_TAG):$(DOCKER_VER)
