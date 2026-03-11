# Wisecow on Kubernetes

Assessment submission for containerizing and deploying the `wisecow` application with Kubernetes, CI/CD, TLS, and supporting DevOps scripts.

## Included artifacts

- `Dockerfile`: production image for the Wisecow shell application
- `deployment.yaml`: namespace, deployment, and service manifests
- `ingress.yaml`: NGINX ingress with TLS
- `.github/workflows/main.yml`: image build/push and cluster deployment workflow
- `system_health_monitor.py`: Problem Statement 2 objective 1
- `log_file_analyzer.py`: Problem Statement 2 objective 3
- `app_health_checker.py`: extra utility for Problem Statement 2 objective 4
- `ksp-wisecow-zero-trust.yaml`: optional KubeArmor zero-trust policy

## Local container build

```bash
docker build -t wisecow:local .
docker run --rm -p 4499:4499 wisecow:local
```

Open `http://localhost:4499`.

## Kubernetes deployment

Apply the manifests after updating the image reference or letting CI render it during deployment:

```bash
kubectl apply -f deployment.yaml
kubectl -n wisecow create secret tls wisecow-tls --cert=tls.crt --key=tls.key
kubectl apply -f ingress.yaml
```

For local testing with Kind or Minikube, map `wisecow.local` to your ingress IP in `/etc/hosts`.

## TLS

The ingress expects a TLS secret named `wisecow-tls`. The GitHub Actions deployment job recreates that secret from repository secrets:

- `TLS_CRT`: PEM encoded certificate
- `TLS_KEY`: PEM encoded private key

For a self-signed local certificate:

```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout tls.key \
  -out tls.crt \
  -subj "/CN=wisecow.local/O=wisecow"
```

## GitHub Actions workflow

The workflow:

1. Builds the Docker image on every push and pull request.
2. Pushes the image to `ghcr.io/<owner>/wisecow` on non-PR runs.
3. Deploys to a self-hosted runner with `kubectl` access to the target cluster.
4. Updates the Kubernetes deployment with the new image and applies the ingress.

## Problem Statement 2 scripts

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

System health monitor:

```bash
python3 system_health_monitor.py --cpu-threshold 80 --memory-threshold 80 --disk-threshold 80
python3 system_health_monitor.py --watch --interval 60
```

Log file analyzer:

```bash
python3 log_file_analyzer.py /var/log/nginx/access.log --top 5
```

Application health checker:

```bash
python3 app_health_checker.py https://wisecow.local
```

## Optional KubeArmor policy

Apply the zero-trust policy after KubeArmor is installed:

```bash
kubectl apply -f ksp-wisecow-zero-trust.yaml
```
