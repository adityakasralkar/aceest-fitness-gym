# ACEest Fitness & Gym — DevOps CI/CD Pipeline

![CI/CD Pipeline](https://github.com/adityakasralkar/aceest-fitness-gym/actions/workflows/main.yml/badge.svg)

> A production-grade Flask REST API for fitness and gym management, built with modern DevOps practices including automated CI/CD pipelines, containerization, and continuous testing.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Flask 3.0, Python 3.11 |
| Database | SQLite (dev) / PostgreSQL (prod) |
| ORM | SQLAlchemy |
| Testing | Pytest |
| Containerization | Docker |
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
│   │   │   ├── clients.py
│   │   │   └── programs.py
│   │   ├── models/
│   │   │   └── database.py
│   │   └── services/
│   │       └── calculator.py
│   ├── tests/
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

## API Endpoints

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
python -m pytest tests/ -v
```

14 tests covering calculator logic and client API endpoints.

---

## Docker
```bash
# Build
docker build -t aceest-backend ./backend

# Run
docker run -p 5000:5000 -e DATABASE_URL=sqlite:///aceest.db aceest-backend

# Run with PostgreSQL
docker-compose up --build
```

---

## CI/CD Pipeline

### GitHub Actions
Triggers on every push to `main` or `dev`.
```
Push to GitHub
      ↓
Job 1: Build & Test → Install deps → Run 14 Pytest tests
      ↓
Job 2: Docker Build → Build image → Run tests inside container
```

### Jenkins BUILD
Secondary build validation environment.
```
Stage 1: Checkout      → Pull code from GitHub
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
BITS Pilani — S2 2025