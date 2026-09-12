# Kubernetes manifests for nebula-dashboard

ArgoCD watches this folder and auto-syncs it to the `dashboard` namespace.

**Note:** `dashboard-secret` (DB credentials) is intentionally NOT included here.
Secrets are created manually and kept out of Git:

kubectl create secret generic dashboard-secret \
  --from-literal=DB_PASSWORD='<value>' \
  --from-literal=DB_ROOT_PASSWORD='<value>' \
  -n dashboard
