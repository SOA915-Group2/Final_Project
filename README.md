# 🧩 Microservices-Based Application

## 📌 Overview

This project implements a fully containerized, cloud-native microservices architecture on Kubernetes (GKE). It includes independent services for identity, product, order, and frontend UI, integrated with centralized logging (EFK stack) and monitoring (Prometheus & Grafana). CI/CD is automated via GitHub Actions.


## 🧱 Architecture
System Diagram
<img width="973" height="719" alt="image" src="https://github.com/user-attachments/assets/bec1badf-b3e7-4c11-9568-d56d5e19e674" />





## Microservices Implemented:

- Identity Service – Registration, authentication, and user profile management.
- Product Service – Catalog management and product data operations.
- Order Service – User orders and transaction handling.
- Frontend Service – Frontend UI.

## Tech Stack:

- Backend: FastAPI, PostgreSQL/MongoDB
- Frontend: React + TailwindCSS
- Containerization: Docker
- Orchestration: Kubernetes (GKE)
- Monitoring: Prometheus, Grafana
- Logging: Fluentd, Elasticsearch, Kibana
- CI/CD: GitHub Actions

## 🚀 Deployment Guide

Prerequisites
- Docker
- Docker Compose
- kubectl
- Git

## ⚙️ Kubernetes Deployment



### 1. **Create GKE Cluster & Namespace**
```bash
gcloud container clusters get-credentials <CLUSTER_NAME> --region <REGION>
kubectl create namespace microservice-app
```

### 2. Deploy Microservices
```bash
kubectl apply -f k8s/identity/
kubectl apply -f k8s/product/
kubectl apply -f k8s/order/
kubectl apply -f k8s/frontend/
```

### 3. Deploy Logging Stack (EFK)
```bash
kubectl apply -f k8s/logging/elasticsearch.yaml
kubectl apply -f k8s/logging/fluentd.yaml
kubectl apply -f k8s/logging/kibana.yaml
```

### 4. Deploy Monitoring Stack (Prometheus & Grafana)
```bash
kubectl apply -f k8s/monitoring/prometheus.yaml
kubectl apply -f k8s/monitoring/grafana.yaml
```

### 5. Expose Services via Ingress
```bash
kubectl apply -f k8s/ingress/nginx-resource.yaml
```

## 🌐 External Access URLs

| Component | URL |
| ------ | ------ |
| Frontend | http://<INGRESS_IP>/ |
| Kibana | http://<INGRESS_IP>/kibana |
| Grafana | http://<INGRESS_IP>/grafana |
| Prometheus | http://<INGRESS_IP>/prometheus |

Replace <INGRESS_IP> with kubectl get ingress result.


## 🔧 Microservices Details

### 1. Identity Service
- Endpoints:
- POST /register
- POST /login
- GET /profile/{id}

### 2. Product Service
- Endpoints:
- GET /products
- POST /products
- GET /products/{id}


## ✅ Testing
- Unit tests: Located in /tests/unit
- Integration tests: Validate API interaction between services
- End-to-end tests: Test full application flow using Postman/Newman

- To run in Kubernetes:
```bash
kubectl apply -f k8s/service_test/unit/test_identity.yaml
kubectl apply -f k8s/service_test/unit/test_order.yaml
kubectl apply -f k8s/service_test/unit/test_product.yaml
```

## 🔄 CI/CD Pipeline
GitHub Actions handles build, test, and deploy:

Workflow Jobs
- Build: Docker build & push to Google Artifact Registry
- Test: Kubernetes pod runs unit/integration tests
- Deploy: kubectl apply to GKE

Secrets Required
- GCP_PROJECT_ID
- GCP_ARTIFACT_JSON
- GCP_CLUSTER_NAME
- GCP_REGION

## 📊 Monitoring with Prometheus & Grafana
- Prometheus scrapes metrics from services and stores time-series data.
- Grafana dashboards visualize pod metrics, HTTP traffic, CPU/Memory usage.
- Prometheus ServiceMonitors/targets configured via prometheus.yaml.

## 📂 Folder Structure
```bash
.
├── k8s
│   ├── deployments
│   ├── frontend
│   ├── identity
│   ├── ingress
│   ├── logging
│   ├── monitoring
│   ├── order
│   ├── product
│   └── service_test
│       ├── e2e
│       ├── integration
│       └── unit
├── src
│   ├── frontend
│   ├── identity-service
│   ├── order-service
│   └── product-service
└── tests
    ├── integration
    ├── unit
    └── e2e
```


## 👥 Contributors
- Shuai Zhang
- Aashish Suwal
- Bijay Adhikari
- Sagar Baral

## 📚 License

MIT License
