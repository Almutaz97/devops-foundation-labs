#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

RELEASE_NAME="${RELEASE_NAME:-minimal-api}"
NAMESPACE="${NAMESPACE:-minimal-api-helm}"
CHART_PATH="${CHART_PATH:-${PROJECT_DIR}/helm/minimal-api}"

command -v kubectl >/dev/null 2>&1 || {
  echo "Error: kubectl is required." >&2
  exit 1
}

command -v helm >/dev/null 2>&1 || {
  echo "Error: helm is required." >&2
  exit 1
}

kubectl cluster-info >/dev/null

echo "Validating Helm chart..."
helm lint "$CHART_PATH"

echo "Installing Helm release..."
helm upgrade --install "$RELEASE_NAME" "$CHART_PATH" \
  --namespace "$NAMESPACE" \
  --create-namespace \
  --wait \
  --timeout 5m

echo
echo "Deployed resources:"
kubectl -n "$NAMESPACE" get \
  deployment,statefulset,pods,services,pvc
