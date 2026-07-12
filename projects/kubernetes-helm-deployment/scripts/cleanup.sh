#!/usr/bin/env bash
set -Eeuo pipefail

RELEASE_NAME="${RELEASE_NAME:-minimal-api}"
NAMESPACE="${NAMESPACE:-minimal-api-helm}"

if helm status "$RELEASE_NAME" \
  --namespace "$NAMESPACE" >/dev/null 2>&1; then

  echo "Uninstalling Helm release..."
  helm uninstall "$RELEASE_NAME" \
    --namespace "$NAMESPACE" \
    --wait
else
  echo "Helm release is not installed."
fi

echo "Deleting namespace..."
kubectl delete namespace "$NAMESPACE" \
  --ignore-not-found \
  --wait=true

echo "Cleanup completed."
