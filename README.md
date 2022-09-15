# Observability Project

## Overview

The purpose of this project is to demonstrate a basic implementation of observability for a given application.

## Tech Stack

- Python/Flask for application
- OpenTelemetry Python SDK for instrumenting telemetry data (tracers, signals, logs)
- OpenTelemetry Collector for receiving/processing/exporting telemetry data
- Jaeger for Tracer Monitoring
- Prometheus for Metrics
- Grafana/Loki for centralized Logging (not implemented)
- Helm

## High Level Architecture

![architecture](https://github.com/corykitchens/observability-project/blob/main/images/arch.png?raw=true)

## Implemented Functionality

TODO

## Functionality Not Implemented

- Logging Telemtry in Application
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
