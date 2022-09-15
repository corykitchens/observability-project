
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

install:
	helm upgrade --install app infra/app

uninstall:
	helm uninstall app

jaeger:
	kubectl port-forward --namespace observability svc/jaeger-query 16686

prometheus:
	kubectl port-forward --namespace default svc/prometheus-kube-prometheus-prometheus 9090:9090

app:
	kubectl port-forward --namespace default svc/app 5000

local:
	opentelemetry-instrument \
	--traces_exporter console \
	--metrics_exporter console \
	flask run
