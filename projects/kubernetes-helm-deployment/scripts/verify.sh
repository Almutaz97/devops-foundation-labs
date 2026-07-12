#!/usr/bin/env bash
set -Eeuo pipefail

NAMESPACE="${NAMESPACE:-minimal-api-helm}"
SERVICE_NAME="${SERVICE_NAME:-minimal-api-minimal-api}"
CURL_IMAGE="${CURL_IMAGE:-curlimages/curl}"

request_endpoint() {
  local pod_name="$1"
  local endpoint="$2"

  kubectl -n "$NAMESPACE" delete pod "$pod_name" \
    --ignore-not-found \
    --wait=true >/dev/null 2>&1 || true

  kubectl -n "$NAMESPACE" run "$pod_name" \
    --rm \
    --stdin \
    --restart=Never \
    --image="$CURL_IMAGE" \
    --command -- \
    curl --fail --silent --show-error \
    "http://${SERVICE_NAME}${endpoint}"
}

echo "Waiting for the application Deployment..."
kubectl -n "$NAMESPACE" wait \
  --for=condition=Available \
  deployment/minimal-api-minimal-api \
  --timeout=180s

echo "Waiting for PostgreSQL..."
kubectl -n "$NAMESPACE" wait \
  --for=condition=Ready \
  pod/minimal-api-minimal-api-postgres-0 \
  --timeout=180s

echo
echo "Health endpoint:"
request_endpoint minimal-api-health-check /health

echo
echo "Readiness endpoint:"
request_endpoint minimal-api-readiness-check /ready

echo
echo "Database connectivity endpoint:"
request_endpoint minimal-api-database-check /db-health

echo
echo "All verification checks passed."
