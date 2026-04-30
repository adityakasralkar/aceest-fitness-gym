# Devops Assignment
**Aditya Kasralkar**  
**BITS Id: 2024tm93619**

# ACEest Fitness & Gym — DevOps CI/CD Pipeline

![CI/CD Pipeline](https://github.com/adityakasralkar/aceest-fitness-gym/actions/workflows/main.yml/badge.svg)

> A production-grade Flask REST API for fitness and gym management, built with modern DevOps practices including automated CI/CD pipelines, containerization, and continuous testing.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Flask 3.0, Python 3.11 |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Authentication | JWT, Flask-Bcrypt |
| Rate Limiting | Flask-Limiter |
| Testing | Pytest |
| Containerization | Docker & Docker Compose |
| CI/CD | GitHub Actions + Jenkins |
| Version Control | Git / GitHub |

---

## Project Structure
```
aceest-fitness-gym/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── clients.py
│   │   │   └── programs.py
│   │   ├── models/
│   │   │   └── database.py
│   │   └── services/
│   │       └── calculator.py
│   ├── tests/
│   │   ├── test_auth.py
│   │   ├── test_calculator.py
│   │   └── test_clients.py
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── .github/
│   └── workflows/
│       └── main.yml
├── Jenkinsfile
├── docker-compose.yml
└── README.md
```

---

## Local Setup

### Prerequisites
- Python 3.11+
- Docker Desktop
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/adityakasralkar/aceest-fitness-gym.git
cd aceest-fitness-gym
```

### 2. Install Dependencies
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
cp .env.example .env
```

### 4. Run the Application
```bash
python app.py
```

API runs at `http://localhost:5000`

---

## Running Tests Manually

### Prerequisites
- Ensure dependencies are installed (from step 2 above)
- Ensure the application is not running (to avoid port conflicts)

### Run All Tests
```bash
cd backend
python -m pytest tests/ -v
```

### Run Specific Test File
```bash
cd backend
python -m pytest tests/test_auth.py -v
```

### Run Tests with Coverage
```bash
cd backend
python -m pytest tests/ --cov=app --cov-report=html
```

---

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | User login |
| POST | `/api/auth/refresh` | Refresh access token |
| GET | `/api/auth/me` | Get current user info |
| POST | `/api/auth/logout` | Logout user |

### Programs
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/programs/` | Get all programs |
| GET | `/api/programs/<name>` | Get single program |
| POST | `/api/programs/calculate` | Calculate calories |

### Clients
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/clients/` | Get all clients |
| GET | `/api/clients/<name>` | Get single client |
| POST | `/api/clients/` | Create client |
| PUT | `/api/clients/<name>` | Update client |
| DELETE | `/api/clients/<name>` | Delete client |

### Example
```bash
curl -X POST http://localhost:5000/api/clients/ \
  -H "Content-Type: application/json" \
  -d '{"name": "John", "age": 25, "weight": 75, "program": "Fat Loss (FL)"}'
```

---

## Running Tests
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python -m pytest tests/ -v
```

37 tests covering health checks, authentication, calculator logic, and API endpoints.

---

## Docker
```bash
# Start both database and backend with a single command
docker-compose up --build

# Or run in background
docker-compose up -d --build

# Stop services
docker-compose down
```

The application will be available at `http://localhost:5001` with PostgreSQL database running on `localhost:5432`.

---

## CI/CD Integration Overview

### GitHub Actions Workflow
The GitHub Actions pipeline (`.github/workflows/main.yml`) automates the build, test, and containerization process:

- **Triggers**: Runs on every push to `main` or `dev` branches, and on pull requests to `main`.
- **Build & Test Job**: 
  - Sets up Python 3.11 environment
  - Installs dependencies from `requirements.txt`
  - Executes the full test suite using Pytest
- **Docker Build Job**: 
  - Builds the Docker image from the `backend/Dockerfile`
  - Runs tests inside the container to ensure containerized functionality
- **Purpose**: Ensures code quality and deployability on every change

### Jenkins Pipeline
The Jenkins pipeline (`Jenkinsfile`) provides secondary validation and can be extended for deployment:

- **Stages**:
  1. **Checkout**: Pulls code from the GitHub repository
  2. **Install Dependencies**: Upgrades pip and installs Python packages
  3. **Run Tests**: Executes Pytest test suite
  4. **Docker Build**: Creates the Docker image for the backend
- **Post Actions**: Cleans workspace and reports build status
- **Purpose**: Provides an alternative CI environment and foundation for deployment automation

Both pipelines ensure that code changes are validated through automated testing and containerization before integration.
Stage 2: Install Deps  → pip install requirements
Stage 3: Run Tests     → Execute Pytest suite
Stage 4: Docker Build  → Build and verify image
```

Jenkins setup:
```bash
docker run -d \
  --name jenkins \
  -p 8080:8080 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins/jenkins:lts
```

Access at `http://localhost:8080`

---

## Branch Strategy
```
main     ← production-ready (GitHub Actions + Jenkins)
dev      ← integration branch (GitHub Actions)
feature/ ← individual features
```

---

## CI/CD and Kubernetes Extension

Current extension branch:
```bash
feature/cicd-k8s
```

Jenkins auto-trigger validation note: push a small commit to `feature/cicd-k8s` and wait 2-3 minutes for SCM polling.

Docker Hub image:
```bash
adityakasralkar/aceest-fitness-gym
```

### Health Check
```bash
curl http://localhost:5000/health
```

Example response:
```json
{
  "status": "ok",
  "service": "aceest-fitness-gym",
  "environment": "production",
  "version": "latest",
  "deployment_variant": "stable"
}
```

### Docker Smoke Test
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

### Jenkins VM Jobs
Create these Jenkins **Pipeline from SCM** jobs:

| Job | Branch |
|-----|--------|
| `aceest-cicd-feature` | `*/feature/cicd-k8s` |
| `aceest-dev` | `*/dev` |

The Jenkinsfile includes `pollSCM('H/2 * * * *')`, so Jenkins automatically checks GitHub about every 2 minutes even when GitHub webhooks cannot reach the college VM.

### Optional Tooling Phases
```bash
# Start SonarQube with Docker
docker compose -f docker-compose.sonar.yml up -d

# Start Minikube with Docker driver
minikube start --driver=docker --memory=4096 --cpus=2
minikube addons enable ingress
kubectl get nodes

# Quick Kubernetes deploy test
kubectl create namespace aceest
kubectl -n aceest create deployment aceest-backend --image=adityakasralkar/aceest-fitness-gym:latest
kubectl -n aceest expose deployment aceest-backend --port=80 --target-port=5000
kubectl -n aceest port-forward service/aceest-backend 8080:80
```

Detailed setup:
- [Step-by-step execution guide](docs/step-by-step-execution.md)

---

## Assignment Context

Built for **BITS Pilani — Introduction to DevOps (CSIZG514)** demonstrating:
- Git/GitHub version control
- Flask REST API development
- Pytest testing
- Docker containerization
- Jenkins BUILD pipeline
- GitHub Actions CI/CD automation

---

## Author

**Aditya Kasralkar**
2024tm93619
