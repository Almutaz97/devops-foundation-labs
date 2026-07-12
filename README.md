# DevOps Foundation Labs

A hands-on DevOps portfolio demonstrating containerization, CI/CD, Kubernetes, Helm, automation, troubleshooting, and reproducible infrastructure workflows.

Each project is implemented as a practical engineering deliverable with documentation, verification steps, automation scripts, and evidence of successful operation.

## Portfolio Highlights

- Linux and service-management fundamentals
- Containerized Python application with PostgreSQL
- Docker Compose development environment
- Automated testing with Pytest
- CI/CD pipelines with GitHub Actions
- Container image publishing to GitHub Container Registry
- Semantic releases and rollback workflows
- Kubernetes Deployments and StatefulSets
- Persistent storage using PersistentVolumeClaims
- ConfigMaps and Secrets
- Startup, readiness, and liveness probes
- Resource requests and limits
- Container security contexts
- Reusable Helm charts
- Helm installation, upgrade, rollback, and cleanup
- Automated validation and troubleshooting evidence

## Featured Projects

### Minimal DevOps Workload API

A containerized Flask API designed as a reusable workload for DevOps experiments.

**Key capabilities:**

- Flask and Gunicorn
- PostgreSQL integration
- Docker and Docker Compose
- Health and readiness endpoints
- Prometheus metrics
- Structured JSON logging
- Automated Pytest test suite

**Project directory:**

```text
projects/minimal-devops-workload-api/
```

---

### CI/CD and Docker Release Pipeline

A GitHub Actions workflow that validates, builds, tests, and publishes the application container image.

**Key capabilities:**

- Automated Python tests
- Docker image build validation
- Container smoke testing
- GitHub Container Registry publishing
- Commit-SHA image tags
- Semantic version tags
- Release and rollback workflow

**Published image:**

```text
ghcr.io/almutaz97/minimal-devops-workload-api:v0.2.0
```

---

### Kubernetes and Helm Deployment

A complete Kubernetes deployment of the Flask API and PostgreSQL using raw manifests and a reusable Helm chart.

**Key capabilities:**

- Dedicated Kubernetes namespaces
- Application Deployment with multiple replicas
- PostgreSQL StatefulSet
- ClusterIP and headless Services
- PersistentVolumeClaim
- ConfigMap and Secret integration
- Startup, readiness, and liveness probes
- CPU, memory, and ephemeral-storage controls
- Non-root application container
- Restricted container security contexts
- Helm chart templates and values
- Fresh installation
- Helm upgrade and rollback
- Persistent-storage verification
- Automated installation, verification, and cleanup
- GitHub Actions Helm validation
- Documented troubleshooting incident

**Project directory:**

```text
projects/kubernetes-helm-deployment/
```

**Detailed documentation:**

- [Project README](projects/kubernetes-helm-deployment/README.md)
- [Architecture](projects/kubernetes-helm-deployment/docs/architecture.md)
- [Verification evidence](projects/kubernetes-helm-deployment/docs/evidence.md)
- [Troubleshooting](projects/kubernetes-helm-deployment/docs/troubleshooting.md)

## Repository Structure

```text
.
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── project-4-helm-validation.yml
├── docs/
├── projects/
│   ├── project-0-devops-foundation/
│   ├── minimal-devops-workload-api/
│   └── kubernetes-helm-deployment/
├── shared/
│   └── scripts/
└── README.md
```

## Engineering Approach

Every portfolio project aims to include:

1. A clearly defined engineering objective
2. Reproducible implementation steps
3. Automated validation
4. Health and failure verification
5. Security-conscious configuration
6. Troubleshooting documentation
7. Cleanup and rollback procedures
8. Git history showing incremental development

## Validation

The repository uses GitHub Actions to validate relevant projects automatically.

Current automated checks include:

- Python test execution
- Docker build validation
- Helm chart linting
- Helm template rendering
- Kubernetes manifest validation
- Shell script syntax validation
- SonarQube code and security analysis

## Technologies

```text
Linux
Bash
Python
Flask
Gunicorn
PostgreSQL
Docker
Docker Compose
Git
GitHub Actions
GitHub Container Registry
Kubernetes
Minikube
Helm
Prometheus
SonarQube
```

## Getting Started

Clone the repository:

```bash
git clone git@github.com:Almutaz97/devops-foundation-labs.git
cd devops-foundation-labs
```

Open the README inside each project directory for its prerequisites, installation process, verification commands, and cleanup instructions.

## Repository Goal

The goal of this repository is to demonstrate practical DevOps and platform-engineering skills through working, testable, and documented projects rather than isolated configuration examples.
