#!/bin/bash
# Idempotent bootstrap: namespaces, then base charts. Run from repo root or any dir (uses script dir for paths).
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

NAMESPACES=(cluster-tools nvidia onepassword cert-manager edge argocd external-secrets)
for NS in "${NAMESPACES[@]}"; do
  kubectl create ns "$NS" 2>/dev/null || true
  kubectl label ns "$NS" --overwrite pod-security.kubernetes.io/enforce=privileged pod-security.kubernetes.io/enforce-version=latest 2>/dev/null || true
done

helm upgrade --install -n nvidia nvidia-device-plugin nvidia-device-plugin

# 1Password Connect: ensure Secrets exist (token + credentials). Delegates to chart's setup script.
if [[ -f "$SCRIPT_DIR/onepassword-connect/setup.sh" ]]; then
  "$SCRIPT_DIR/onepassword-connect/setup.sh" "$@"
fi

helm upgrade --install -n onepassword --set connect.ingress.enabled=false onepassword-connect onepassword-connect
helm upgrade --install -n edge purelb purelb
helm upgrade --install -n cert-manager cert-manager cert-manager/charts/cert-manager
helm upgrade --install -n edge nginx nginx
helm upgrade --install -n cluster-tools reloader reloader
helm upgrade --install -n cluster-tools kubernetes-replicator kubernetes-replicator
helm upgrade --install -n edge external-dns external-dns/helm
helm upgrade --install -n cert-manager certificates cert-manager/charts/certificates

# Allow 1Password Connect (and operator if present) to become ready before re-install and Argo CD
sleep 300
helm upgrade --install -n onepassword onepassword-connect onepassword-connect -f onepassword-connect/values.yaml

# Wait for 1Password to be ready so Argo CD's OnePasswordItem can sync (avoid starting Argo CD too early)
kubectl wait --for=condition=available deployment --all -n onepassword --timeout=120s 2>/dev/null || true

# Argo CD (repo-creds from 1Password item jd4883; hook labels the synced secret for Argo CD)
ARGOCD_CHART="$SCRIPT_DIR/../argocd/charts/argocd/server"
if [[ -d "$ARGOCD_CHART" ]]; then
  (cd "$ARGOCD_CHART" && helm dependency update)
  helm upgrade --install -n argocd argocd "$ARGOCD_CHART"
fi