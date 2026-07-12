# Troubleshooting

## Incident: PostgreSQL CrashLoopBackOff

### Symptoms

The PostgreSQL pod entered:

```text
CrashLoopBackOff
```

The Flask API containers were running, but their readiness probes returned HTTP 503 because PostgreSQL was unavailable.

PostgreSQL logs showed:

```text
chmod: /var/lib/postgresql/data: Operation not permitted
chmod: /var/run/postgresql: Operation not permitted
initdb: error: could not access directory "/var/lib/postgresql/data": Permission denied
```

### Root Cause

The PostgreSQL container was forced to start directly as UID and GID `999`.

The official PostgreSQL image needs permission during startup to prepare its data and runtime directories before starting the PostgreSQL process.

The forced user configuration prevented the initialization process from changing directory permissions.

### Incorrect Configuration

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 999
  runAsGroup: 999
```

### Resolution

The forced UID and GID settings were removed.

The final PostgreSQL container security context became:

```yaml
securityContext:
  allowPrivilegeEscalation: false
  seccompProfile:
    type: RuntimeDefault
```

The pod-level filesystem group remained enabled:

```yaml
securityContext:
  fsGroup: 999
  fsGroupChangePolicy: OnRootMismatch
```

The PostgreSQL pod was recreated:

```bash
kubectl -n minimal-api delete pod postgres-0
```

### Result

PostgreSQL recovered successfully:

```text
postgres-0   1/1   Running
```

Both application replicas automatically became ready.

The application readiness endpoint returned:

```json
{"database":"reachable","status":"ready"}
```

The existing PersistentVolumeClaim was reused successfully.

### Lesson

Security controls must be compatible with the initialization requirements of the container image. An overly restrictive security context can prevent a valid workload from starting.
