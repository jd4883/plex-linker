#!/bin/bash
# Idempotent bootstrap: namespaces, 1Password Connect (in cluster-tools), replicator, purelb, cert-manager, nginx, external-dns, certificates, then Argo CD.
# Ingress + DNS in core so Terraform can reach 1Password Connect and Argo CD via DNS (no port-forward).
# Argo CD (after Terraform) will adopt these apps and sync from git; other apps (reloader, nvidia-device-plugin, etc.) are Argo CD–only.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

NAMESPACES=(cluster-tools nvidia cert-manager edge argocd)
for NS in "${NAMESPACES[@]}"; do
  kubectl create ns "$NS" 2>/dev/null || true
  kubectl label ns "$NS" --overwrite pod-security.kubernetes.io/enforce=privileged pod-security.kubernetes.io/enforce-version=latest 2>/dev/null || true
done

# 1Password Connect: ensure Secrets exist in cluster-tools (token + credentials).
if [[ -f "$SCRIPT_DIR/onepassword-connect/setup.sh" ]]; then
  OP_NAMESPACE=cluster-tools "$SCRIPT_DIR/onepassword-connect/setup.sh" "$@"
fi

# 1Password Connect first (no ingress) so Connect is starting; then replicator.
helm upgrade --install -n cluster-tools --set connect.ingress.enabled=false onepassword-connect onepassword-connect
helm upgrade --install -n cluster-tools kubernetes-replicator kubernetes-replicator

# Ingress stack: purelb (LB IPs) then nginx (controller); cert-manager before certificates; external-dns for record propagation.
helm upgrade --install -n edge purelb purelb
helm upgrade --install -n cert-manager cert-manager cert-manager/charts/cert-manager
helm upgrade --install -n edge nginx nginx
helm upgrade --install -n edge external-dns external-dns/helm
helm upgrade --install -n cert-manager certificates cert-manager/charts/certificates

# Allow 1Password Connect (and operator) to become ready, then install with full values (ingress enabled).
sleep 300
helm upgrade --install -n cluster-tools onepassword-connect onepassword-connect -f onepassword-connect/values.yaml

# Wait for 1Password so Argo CD's OnePasswordItem can sync (avoid starting Argo CD too early).
kubectl wait --for=condition=available deployment --all -n cluster-tools --timeout=120s 2>/dev/null || true

# Argo CD; after this, run Terraform to create Projects/Applications; Argo CD will sync and adopt the above apps.
ARGOCD_CHART="$SCRIPT_DIR/../argocd/charts/argocd/server"
if [[ -d "$ARGOCD_CHART" ]]; then
  (cd "$ARGOCD_CHART" && helm dependency update)
  helm upgrade --install -n argocd argocd "$ARGOCD_CHART"
fi