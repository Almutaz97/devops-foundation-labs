# Architecture

This project deploys a stateless Flask API and a stateful PostgreSQL database on Kubernetes.

## Request Flow

```text
Client or verification pod
            |
            v
Application ClusterIP Service
            |
            v
Flask API Deployment
     2 replicas
            |
            v
PostgreSQL Headless Service
            |
            v
PostgreSQL StatefulSet
            |
            v
PersistentVolumeClaim
```

## Application Deployment

The Flask API runs as a Kubernetes Deployment with:

- Two replicas by default
- RollingUpdate deployment strategy
- Startup probe on `/health`
- Readiness probe on `/ready`
- Liveness probe on `/health`
- CPU and memory requests and limits
- Non-root execution
- Read-only root filesystem
- Disabled privilege escalation
- Dropped Linux capabilities
- A writable temporary `/tmp` volume

## PostgreSQL StatefulSet

PostgreSQL runs as a single-replica StatefulSet with:

- Stable pod identity
- Headless Kubernetes Service
- PersistentVolumeClaim
- Startup, readiness, and liveness probes
- CPU and memory requests and limits
- Persistent data across pod recreation

## Configuration

Non-sensitive application configuration is stored in a ConfigMap.

Database credentials are stored in a Kubernetes Secret.

The real local Secret file is excluded from Git using `.gitignore`.

## Helm Chart

The Helm chart makes the following settings configurable:

- Application replica count
- Application image repository and tag
- Service type and ports
- Application environment
- Database credentials
- PostgreSQL image
- Persistent storage size
- StorageClass
- Application resources
- PostgreSQL resources
