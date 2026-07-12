# Kubernetes and Helm Deployment

A production-style Kubernetes deployment of a containerized Flask API with PostgreSQL, implemented using both raw Kubernetes manifests and a reusable Helm chart.

This project demonstrates application deployment, persistent database storage, Kubernetes configuration management, health probes, resource controls, container security, Helm upgrades, rollbacks, troubleshooting, and reproducible verification.

## Project Overview

The deployed system contains:

* A Flask API running as a Kubernetes Deployment
* Two application replicas by default
* PostgreSQL running as a StatefulSet
* Persistent storage using a PersistentVolumeClaim
* A ClusterIP Service for the application
* A headless Service for PostgreSQL
* ConfigMap-based application configuration
* Secret-based database credentials
* Startup, readiness, and liveness probes
* CPU and memory requests and limits
* Restricted container security contexts
* A configurable Helm chart
* Upgrade and rollback support

The application image is published through the CI/CD project:

```text
ghcr.io/almutaz97/minimal-devops-workload-api:v0.2.0
```

## Architecture

```text
                     Kubernetes Cluster

              ┌─────────────────────────┐
              │ Client or test pod      │
              └────────────┬────────────┘
                           │ HTTP
                           ▼
              ┌─────────────────────────┐
              │ Application Service     │
              │ ClusterIP, port 80      │
              └────────────┬────────────┘
                           │
                 ┌─────────┴─────────┐
                 ▼                   ▼
       ┌──────────────────┐ ┌──────────────────┐
       │ Flask API Pod 1  │ │ Flask API Pod 2  │
       │ Port 8000        │ │ Port 8000        │
       └─────────┬────────┘ └─────────┬────────┘
                 └─────────┬──────────┘
                           │ PostgreSQL
                           ▼
              ┌─────────────────────────┐
              │ PostgreSQL Service      │
              │ Headless, port 5432     │
              └────────────┬────────────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │ PostgreSQL StatefulSet  │
              │ postgres-0              │
              └────────────┬────────────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │ PersistentVolumeClaim   │
              │ 1 GiB                   │
              └─────────────────────────┘
```

More details are available in [docs/architecture.md](docs/architecture.md).

## Application Endpoints

| Endpoint     | Purpose                                           |
| ------------ | ------------------------------------------------- |
| `/health`    | Confirms that the API process is healthy          |
| `/ready`     | Confirms that the API can connect to PostgreSQL   |
| `/db-health` | Returns PostgreSQL connectivity information       |
| `/metrics`   | Exposes Prometheus-compatible application metrics |

## Repository Structure

```text
kubernetes-helm-deployment/
├── README.md
├── k8s/
│   └── raw/
│       ├── 00-namespace.yaml
│       ├── 01-configmap.yaml
│       ├── 02-secret.example.yaml
│       ├── 03-postgres.yaml
│       ├── 04-app-deployment.yaml
│       └── 05-app-service.yaml
├── helm/
│   └── minimal-api/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│           ├── _helpers.tpl
│           ├── configmap.yaml
│           ├── secret.yaml
│           ├── deployment.yaml
│           ├── service.yaml
│           └── postgres.yaml
├── scripts/
│   ├── install.sh
│   ├── verify.sh
│   └── cleanup.sh
└── docs/
    ├── architecture.md
    ├── evidence.md
    └── troubleshooting.md
```

The GitHub Actions workflow is stored at the monorepo root:

```text
.github/workflows/project-4-helm-validation.yml
```

## Prerequisites

The following tools are required:

* A working Kubernetes cluster
* `kubectl`
* Helm
* A default Kubernetes StorageClass

The project was tested with Minikube.

Check the cluster before installation:

```bash
kubectl get nodes
kubectl get storageclass
```

At least one node must be in the `Ready` state, and a default StorageClass must be available.

## Helm Chart Validation

Run Helm linting:

```bash
helm lint helm/minimal-api
```

Expected result:

```text
1 chart(s) linted, 0 chart(s) failed
```

Render the chart locally:

```bash
helm template minimal-api helm/minimal-api \
  --namespace minimal-api-helm \
  > /tmp/minimal-api-rendered.yaml
```

Validate the rendered Kubernetes resources:

```bash
kubectl apply --dry-run=client \
  -f /tmp/minimal-api-rendered.yaml
```

## Helm Installation

Install the release:

```bash
helm install minimal-api helm/minimal-api \
  --namespace minimal-api-helm \
  --create-namespace \
  --wait \
  --timeout 5m
```

Alternatively, use the installation script:

```bash
./scripts/install.sh
```

Check the Helm release:

```bash
helm list -n minimal-api-helm
helm status minimal-api -n minimal-api-helm
```

Check the deployed Kubernetes resources:

```bash
kubectl -n minimal-api-helm get \
  deployment,statefulset,pods,services,pvc
```

Expected workload state:

```text
deployment.apps/minimal-api-minimal-api           2/2
statefulset.apps/minimal-api-minimal-api-postgres 1/1
```

The PostgreSQL PersistentVolumeClaim should show:

```text
STATUS: Bound
```

## Application Verification

Run the automated verification script:

```bash
./scripts/verify.sh
```

The application can also be tested manually from inside the cluster.

### Health endpoint

```bash
kubectl -n minimal-api-helm run curl-test \
  --rm -i \
  --restart=Never \
  --image=curlimages/curl \
  -- curl -s http://minimal-api-minimal-api/health
```

Expected response:

```json
{
  "env": "helm",
  "service": "minimal-devops-workload-api",
  "status": "ok"
}
```

### Readiness endpoint

```bash
kubectl -n minimal-api-helm run curl-test \
  --rm -i \
  --restart=Never \
  --image=curlimages/curl \
  -- curl -s http://minimal-api-minimal-api/ready
```

Expected response:

```json
{
  "database": "reachable",
  "status": "ready"
}
```

### Database connectivity endpoint

```bash
kubectl -n minimal-api-helm run curl-test \
  --rm -i \
  --restart=Never \
  --image=curlimages/curl \
  -- curl -s http://minimal-api-minimal-api/db-health
```

Expected response:

```json
{
  "database": "ok",
  "host": "minimal-api-minimal-api-postgres",
  "name": "minimal_api",
  "port": "5432"
}
```

## Helm Upgrade

The application replica count is configurable through Helm values.

Upgrade the release from two replicas to three:

```bash
helm upgrade minimal-api helm/minimal-api \
  --namespace minimal-api-helm \
  --set replicaCount=3 \
  --wait \
  --timeout 5m
```

Verify the new replica count:

```bash
kubectl -n minimal-api-helm get deployment,pods
```

Expected Deployment state:

```text
deployment.apps/minimal-api-minimal-api   3/3
```

Check the release history:

```bash
helm history minimal-api -n minimal-api-helm
```

The history should contain the original installation and the upgrade:

```text
REVISION  STATUS       DESCRIPTION
1         superseded   Install complete
2         deployed     Upgrade complete
```

## Helm Rollback

Roll back to the original revision:

```bash
helm rollback minimal-api 1 \
  --namespace minimal-api-helm \
  --wait \
  --timeout 5m
```

Verify the rollback:

```bash
helm history minimal-api -n minimal-api-helm
kubectl -n minimal-api-helm get deployment,pods
```

Expected result:

```text
deployment.apps/minimal-api-minimal-api   2/2
```

The Helm history should contain a new deployed rollback revision:

```text
REVISION  STATUS       DESCRIPTION
1         superseded   Install complete
2         superseded   Upgrade complete
3         deployed     Rollback to 1
```

Verify that the application remains ready:

```bash
kubectl -n minimal-api-helm run curl-test \
  --rm -i \
  --restart=Never \
  --image=curlimages/curl \
  -- curl -s http://minimal-api-minimal-api/ready
```

Expected response:

```json
{
  "database": "reachable",
  "status": "ready"
}
```

## Raw Kubernetes Installation

The project also contains raw Kubernetes manifests that deploy the same application without Helm.

Create a local Secret file from the example:

```bash
cp k8s/raw/02-secret.example.yaml \
  k8s/raw/02-secret.local.yaml
```

Edit the local file and replace the placeholder credentials.

The local Secret file is excluded from Git through `.gitignore`.

Apply the manifests in order:

```bash
kubectl apply -f k8s/raw/00-namespace.yaml
kubectl apply -f k8s/raw/01-configmap.yaml
kubectl apply -f k8s/raw/02-secret.local.yaml
kubectl apply -f k8s/raw/03-postgres.yaml
kubectl apply -f k8s/raw/04-app-deployment.yaml
kubectl apply -f k8s/raw/05-app-service.yaml
```

Wait for the workloads:

```bash
kubectl -n minimal-api rollout status \
  statefulset/postgres \
  --timeout=180s

kubectl -n minimal-api rollout status \
  deployment/minimal-api \
  --timeout=180s
```

Verify:

```bash
kubectl -n minimal-api get \
  deployment,statefulset,pods,services,pvc
```

## Persistent Storage Verification

PostgreSQL uses a StatefulSet with a PersistentVolumeClaim.

The PVC can be checked with:

```bash
kubectl -n minimal-api-helm get pvc
```

To verify that storage survives pod recreation, delete the PostgreSQL pod:

```bash
kubectl -n minimal-api-helm delete pod \
  minimal-api-minimal-api-postgres-0
```

The StatefulSet automatically recreates the pod.

Watch the recreation:

```bash
kubectl -n minimal-api-helm get pods -w
```

After the pod returns to `Running`, verify the database:

```bash
kubectl -n minimal-api-helm run curl-test \
  --rm -i \
  --restart=Never \
  --image=curlimages/curl \
  -- curl -s http://minimal-api-minimal-api/db-health
```

The database should remain reachable through the same persistent volume.

## Health Probes

### Application startup probe

The application startup probe checks:

```text
/health
```

It prevents readiness and liveness checks from affecting the container before startup completes.

### Application readiness probe

The readiness probe checks:

```text
/ready
```

This endpoint verifies both the application and PostgreSQL connection.

A pod is removed from the Service endpoints when the database is unavailable.

### Application liveness probe

The liveness probe checks:

```text
/health
```

Kubernetes restarts the application container if the process becomes unhealthy.

### PostgreSQL probes

PostgreSQL uses `pg_isready` for startup, readiness, and liveness checks.

## Resource Management

Both the application and PostgreSQL define CPU and memory requests and limits.

Application defaults:

```yaml
resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 256Mi
```

PostgreSQL defaults:

```yaml
resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 512Mi
```

## Security Controls

The application container uses the following security controls:

* Runs as a non-root user
* Uses a fixed non-root UID and GID
* Disables privilege escalation
* Drops all Linux capabilities
* Uses the default seccomp profile
* Uses a read-only root filesystem
* Mounts a temporary writable `/tmp` directory

PostgreSQL uses a security context that remains compatible with the initialization behavior of the official PostgreSQL image and persistent storage.

Local Kubernetes Secret files are excluded from Git.

For a real production environment, credentials should be supplied through a secure secret-management system rather than stored in a public values file.

## Troubleshooting Evidence

During development, PostgreSQL entered `CrashLoopBackOff`.

The logs showed:

```text
chmod: /var/lib/postgresql/data: Operation not permitted
initdb: error: could not access directory "/var/lib/postgresql/data": Permission denied
```

The root cause was an overly restrictive container security context that forced PostgreSQL to start directly as UID and GID `999`.

The official PostgreSQL image needs permission during startup to prepare its data and runtime directories.

The forced UID and GID configuration was removed while retaining:

* Disabled privilege escalation
* RuntimeDefault seccomp profile
* Pod filesystem group configuration

After the PostgreSQL pod was recreated:

* PostgreSQL became ready
* Both API replicas became ready
* The `/ready` endpoint returned HTTP 200
* The existing PersistentVolumeClaim was reused

The complete incident is documented in [docs/troubleshooting.md](docs/troubleshooting.md).

## Cleanup

Remove the Helm release and namespace:

```bash
./scripts/cleanup.sh
```

The equivalent manual commands are:

```bash
helm uninstall minimal-api \
  --namespace minimal-api-helm

kubectl delete namespace minimal-api-helm
```

Remove the raw Kubernetes deployment:

```bash
kubectl delete namespace minimal-api
```

## Automated Validation

GitHub Actions validates the project when relevant files are pushed or changed in a pull request.

The workflow performs:

* Helm chart linting
* Helm template rendering
* Rendered Kubernetes manifest validation
* Shell script syntax validation

Workflow location:

```text
.github/workflows/project-4-helm-validation.yml
```

## Verified Results

The following operations have been tested successfully:

* Raw Kubernetes deployment
* Application Deployment with two replicas
* PostgreSQL StatefulSet
* Application and PostgreSQL Services
* ConfigMap and Secret injection
* PersistentVolumeClaim binding
* Application-to-PostgreSQL connectivity
* Startup, readiness, and liveness probes
* Resource requests and limits
* Container security contexts
* Helm linting
* Helm template rendering
* Kubernetes client-side dry run
* Fresh Helm installation
* Helm upgrade from two to three replicas
* Helm rollback from three to two replicas
* Application readiness after rollback
* PostgreSQL pod recreation with persistent storage
* Real Kubernetes troubleshooting and recovery

## Documentation

* [Architecture](docs/architecture.md)
* [Verification Evidence](docs/evidence.md)
* [Troubleshooting](docs/troubleshooting.md)

## Release

The final verified project release will be tagged:

```text
v1.0.0
```

