# Verification Evidence

## Helm Static Validation

The Helm chart passed linting:

```text
==> Linting helm/minimal-api
1 chart(s) linted, 0 chart(s) failed
```

The chart rendered successfully using `helm template`.

The rendered resources also passed Kubernetes client-side dry-run validation.

## Fresh Helm Installation

The release installed successfully:

```text
NAME: minimal-api
NAMESPACE: minimal-api-helm
STATUS: deployed
REVISION: 1
DESCRIPTION: Install complete
```

## Kubernetes Workloads

The application Deployment reached:

```text
deployment.apps/minimal-api-minimal-api   2/2
```

The PostgreSQL StatefulSet reached:

```text
statefulset.apps/minimal-api-minimal-api-postgres   1/1
```

The PostgreSQL PersistentVolumeClaim reached `Bound` state with 1 GiB of storage.

## Application Endpoint Verification

Health endpoint:

```json
{"env":"helm","service":"minimal-devops-workload-api","status":"ok"}
```

Readiness endpoint:

```json
{"database":"reachable","status":"ready"}
```

Database connectivity endpoint:

```json
{"database":"ok","host":"minimal-api-minimal-api-postgres","name":"minimal_api","port":"5432"}
```

## Helm Upgrade

The application was upgraded from two replicas to three:

```text
REVISION  STATUS       DESCRIPTION
1         superseded   Install complete
2         deployed     Upgrade complete
```

The Deployment reached:

```text
deployment.apps/minimal-api-minimal-api   3/3
```

## Helm Rollback

The release was rolled back to revision 1:

```text
REVISION  STATUS       DESCRIPTION
1         superseded   Install complete
2         superseded   Upgrade complete
3         deployed     Rollback to 1
```

The Deployment returned to:

```text
deployment.apps/minimal-api-minimal-api   2/2
```

The application remained ready after rollback:

```json
{"database":"reachable","status":"ready"}
```

## Persistent Storage

The PostgreSQL pod was deleted and recreated while retaining the existing PersistentVolumeClaim.

PostgreSQL reported:

```text
PostgreSQL Database directory appears to contain a database; Skipping initialization
database system is ready to accept connections
```

This demonstrates that the database directory survived pod recreation.
