
APP_NAME="obs"
REGISTRY_NAME="corykitchens"
COMMIT_SHA := $(shell git rev-parse --short head)

build:
	docker image build -t $(APP_NAME) .

tag:
	docker image tag $(APP_NAME):latest $(REGISTRY_NAME)/$(APP_NAME):latest

push:
	docker image push $(REGISTRY_NAME)/$(APP_NAME):latest

publish: tag push

stop:
	docker container stop $(APP_NAME)

rm:
	docker container rm $(APP_NAME)

run:
	docker run --rm --name="$(APP_NAME)" -p 5000:5000 $(APP_NAME):latest

clean: stop rm