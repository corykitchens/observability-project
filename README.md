# Observability Project

## Overview

The purpose of this project is to demonstrate a basic implementation of observability for a given application.

## Tech Stack

- [Flask](https://flask.palletsprojects.com/en/2.2.x/)
- [OpenTelemetry for telementry data](https://opentelemetry.io/)
- [OpenTelemetry Collector for receiving/processing/exporting telemetry data](https://github.com/open-telemetry/opentelemetry-operator)
- [Jaeger for Tracer Monitoring](https://www.jaegertracing.io/)
- [Prometheus for Metrics](https://prometheus.io/)
- [GrafanaLoki for centralized Logging](https://grafana.com/)
- [Helm](https://helm.sh/)

## High Level Architecture

![architecture](https://github.com/corykitchens/observability-project/blob/main/images/arch.png?raw=true)

## Implemented Functionality

**Infrastructure**

- Local kind cluster running various services for observability (OTEL, Prometheus, Jaeger)

**Trace**

- Trace/Spans created/generated throughout the lifecycle of Application request/response
- App tracers shipped to OTEL Collector
- OTEL Collector shipping traces to Jaeger
- Traces viewable in Jaeger

**Metric**

- A Request Count Metric generated
- Application Metric + System Level metrics shipped to OTEL Collector
- OTEL Collector shipping metrics to Prometheus
- Metrics viewable in Prometheus

## Functionality Not Implemented

**App**

- Test coverage :)

**Traces**

- Injecting Service Name in Tracer

**Metrics**

- Counter Metric for successful/unsuccesful requests
- Histogram for some higher-level cardinality (user-agent, location, payload) etc

**Logging**

- Implement OTEL Logging APIs
- Shipping logs to OTEL Collector
- Shipping logs from OTEL Collector to Loki/Grafana
- Grafana/Loki Deployment

## Production Considerations

![architecture](https://github.com/corykitchens/observability-project/blob/main/images/prod.png?raw=true)

The architecture diagram demonstratoes a `production-grade` deployment of the observability stack given no time or money constraints.

- A centralized observability cluster that contains services related to observability
- A centralied CI/CD cluster that contains services related to the deployment of applications and services to various remote cluters
- A workload cluster that hosts product-specific services

## Deployment Instructions

### Pre-Reqs

- Access to a K8s cluster
- cert-manager
- Jaeger Operator
- OTEL Collector Operator
- Prometheus Deployment

**cert_manager**

```sh
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.9.1/cert-manager.yaml
```

**OTEL Collector Operator**

```sh
kubectl apply -f https://github.com/open-telemetry/opentelemetry-operator/releases/latest/download/opentelemetry-operator.yaml
```

**Jaeger Operator**

```sh
kubectl create namespace observability
kubectl create -f https://github.com/jaegertracing/jaeger-operator/releases/download/v1.37.0/jaeger-operator.yaml -n observability
```

**Prometheus**

```sh
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install my-release bitnami/kube-prometheus
```

**Jaeger/OTEL Collector Deployments**

```sh
kubectl apply -f infra/prereqs/
```

**Build the image**

```
make build
```

**Tag and Publish to Docker Register**

```
make publish
```

**Install Application helm chart into cluster**

```
make install
```
