# Step-by-Step Local + Jenkins Setup

Follow these steps in order. This file is the single runbook for local setup and Jenkins setup.

## 1. Check Branch

```bash
git branch --show-current
```

Expected output:

```text
feature/cicd-k8s
```

## 2. Run App Checks Locally

```bash
cd backend
source venv/bin/activate
python -m pytest tests/ -v
python -m black --check .
python -m flake8 .
cd ..
```

## 3. Manual Docker Smoke Test

Start Docker Desktop first.

```bash
docker build \
  --build-arg APP_VERSION=local-smoke \
  --build-arg DEPLOYMENT_VARIANT=docker-smoke \
  -t adityakasralkar/aceest-fitness-gym:local-smoke \
  ./backend

docker run --rm -d \
  --name aceest-smoke \
  -p 5050:5000 \
  -e FLASK_ENV=testing \
  -e APP_VERSION=local-smoke \
  -e DEPLOYMENT_VARIANT=docker-smoke \
  adityakasralkar/aceest-fitness-gym:local-smoke

curl http://127.0.0.1:5050/health
docker rm -f aceest-smoke
```

## 4. Push Feature Branch

```bash
git push -u origin feature/cicd-k8s
```

## 5. Configure Jenkins Jobs (College VM)

Create two Jenkins jobs as `Pipeline from SCM`:

1. `aceest-cicd-feature` with branch `*/feature/cicd-k8s`
2. `aceest-dev` with branch `*/dev`

Common settings:

1. Repo URL: `git@github.com-personal:adityakasralkar/aceest-fitness-gym.git`
2. Script path: `Jenkinsfile`
3. Build once manually to load pipeline trigger

Jenkinsfile already has `pollSCM('H/2 * * * *')`, so it checks every ~2 minutes.

## 6. Verify Auto Trigger

Make a tiny commit on `feature/cicd-k8s`, push, and wait 2–3 minutes.

Expected:

1. `aceest-cicd-feature` starts automatically.
2. Jenkins log shows latest commit SHA.

After merge to `dev`, `aceest-dev` should auto-run the same way.

## 7. Docker Hub Setup

In Docker Hub:

1. Create repo `adityakasralkar/aceest-fitness-gym`.
2. Create a personal access token.

In Jenkins credentials:

1. Add `dockerhub-credentials` as username/password.
2. Username: `adityakasralkar`
3. Password: Docker Hub token

Run build with:

```text
PUSH_TO_DOCKERHUB=true
RUN_SONARQUBE=false
```

## 8. SonarQube Local Setup With Docker

```bash
docker compose -f docker-compose.sonar.yml up -d
```

Open `http://localhost:9000` and log in with `admin/admin`. Then:

1. Change admin password.
2. Create project key `aceest-fitness-gym`.
3. Create token.

In Jenkins:

1. Configure SonarQube server name `ACEest SonarQube`.
2. Ensure `sonar-scanner` is installed in Jenkins tools.
3. Run build with `RUN_SONARQUBE=true`.

## 9. Minikube Local Setup (Manual)

Install tools:

1. `minikube`
2. `kubectl`

Start cluster:

```bash
minikube start --driver=docker --memory=4096 --cpus=2
minikube addons enable ingress
kubectl get nodes
```

Basic app deploy check:

```bash
kubectl create namespace aceest
kubectl -n aceest create deployment aceest-backend --image=adityakasralkar/aceest-fitness-gym:latest
kubectl -n aceest expose deployment aceest-backend --port=80 --target-port=5000
kubectl -n aceest port-forward service/aceest-backend 8080:80
```

In another terminal:

```bash
curl http://127.0.0.1:8080/health
```

## 10. DOCX Submission Checklist

Prepare a Word report (2–3 pages) with screenshots of:

1. Jenkins auto build on feature branch push
2. Jenkins auto build on merge to `dev`
3. Docker Hub pushed image tags
4. SonarQube quality gate
5. Minikube deployment check (`kubectl get` + `/health`)
