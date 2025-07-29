🧩 Microservices-Based Application

📌 Overview

This project demonstrates the design, development, containerization, orchestration, and monitoring of a microservices-based application. Built using RESTful APIs, Docker, Kubernetes, and integrated with CI/CD and observability tools, the project simulates a real-world system on a local development environment.

🧱 Architecture
System Diagram
<img width="973" height="719" alt="image" src="https://github.com/user-attachments/assets/bec1badf-b3e7-4c11-9568-d56d5e19e674" />





Microservices Implemented:
	Identity Service – Registration, authentication, and user profile management.
 	Product Service – Catalog management and product data operations.
  	Order Service – User orders and transaction handling.
   	Notification Service – Email/SMS notifications for actions.

Tech Stack:
- Backend: Python / Node.js / Java (your choice)
- Databases: PostgreSQL / MongoDB (polyglot persistence per service)
- Containerization: Docker, Docker Compose
- Orchestration: Kubernetes (Minikube / Kind / Docker Desktop)
- CI/CD: GitHub Actions / GitLab CI / Jenkins
- Monitoring: Prometheus, Grafana
- Logging: Fluentd / ELK Stack (if applicable)

🚀 Getting Started

Prerequisites
- Docker
- Docker Compose
- kubectl
- Git

Setup Instructions

1.	Clone the Repository
```sh
   git clone https://github.com/SOA915-Group2/Final_Project.git
   cd Final_Project
```

3.	Run with Docker Compose (Development)
```sh
   docker-compose up --build
```
5.	Run on Kubernetes (Minikube)
```sh
   minikube start
   kubectl apply -f k8s/
```

7.	Monitoring Dashboard (Prometheus + Grafana)
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (Default login: admin/admin)

🔧 Microservices Details

1. Identity Service
- Endpoints:
- POST /register
- POST /login
- GET /profile/{id}

2. Product Service
- Endpoints:
- GET /products
- POST /products
- GET /products/{id}



⚙️ Kubernetes Deployment

Files:
- deployment-user.yaml, deployment-product.yaml
- service-user.yaml, service-product.yaml
- configmap.yaml, secrets.yaml, hpa.yaml

Commands:

```sh
kubectl apply -f k8s/deployment-user.yaml
kubectl get pods
kubectl logs <pod-name>
```

✅ Testing
- Unit tests: Located in /tests/unit
- Integration tests: Validate API interaction between services
- End-to-end tests: Test full application flow using Postman/Newman

🔄 CI/CD Pipeline
- Automated via GitHub Actions
- Steps:
- Lint & Test
- Build Docker images
- Deploy to local Kubernetes cluster
- Notifications via Slack/Email (optional)

📊 Monitoring & Logging
- Prometheus: Application metrics scraping
- Grafana: Dashboard for services
- Logging: Fluentd or ELK integration (optional)

📂 Folder Structure

| Folder Structure |
| ------ |
| ├── src/frontend//|
| ├── src/identity-service/|
| ├── src/order-service/|
| ├── src/product-service/|
| ├── k8s/|
| ├──├── deployments/|
| ├──├── services/|
| ├──├── config/|
| ├── docker-compose.yml|
| ├── README.md|


👥 Contributors
- Shuai Zhang
- Aashish Suwal
- Bijay Adhikari
- Sagar Baral

📚 License

MIT License
