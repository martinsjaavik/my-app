# Connections AI

A full-stack NYT Connections clone with AI-powered hints, auto-solver, leaderboards, puzzle archive, and multiplayer capabilities.

## Features

- **Daily Puzzle**: Play today's Connections puzzle
- **AI Hints**: Get intelligent hints from Llama 3 when you're stuck
- **AI Auto-Solver**: Watch the AI solve puzzles step-by-step
- **Leaderboards**: Track your stats, streaks, and compete globally
- **Puzzle Archive**: Play any past puzzle
- **Multiplayer**: Race friends in real-time

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React + TypeScript + Vite + Tailwind CSS |
| Backend | Python FastAPI |
| AI | Ollama + Llama 3 (8B) |
| Database | PostgreSQL |
| Cache | Redis |
| Infrastructure | Kubernetes/OpenShift + Argo CD |

## Project Structure

```
my-app/
├── frontend/          # React TypeScript app
├── backend/           # Python FastAPI app
├── k8s/               # Kubernetes manifests
│   ├── base/          # Base Kustomize manifests
│   └── overlays/      # Environment-specific configs
└── argocd/            # Argo CD application
```

## Local Development

### Prerequisites

- Node.js 20+
- Python 3.11+
- Docker & Docker Compose
- Ollama (for AI features)

### Quick Start

1. **Start the database and Redis**:
   ```bash
   docker-compose up -d postgres redis
   ```

2. **Start Ollama and pull the model**:
   ```bash
   ollama pull llama3:8b
   ollama serve
   ```

3. **Start the backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

4. **Start the frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

5. **Sync puzzles** (one-time):
   ```bash
   curl -X POST http://localhost:8000/api/v1/puzzles/sync
   ```

The app will be available at http://localhost:3000

## Deployment

### OpenShift with Argo CD

1. Update the image references in `k8s/base/*/deployment.yaml`
2. Update the route hosts in `k8s/base/*/route.yaml`
3. Configure secrets in `k8s/base/secrets/secrets.yaml`
4. Apply the Argo CD application:
   ```bash
   kubectl apply -f argocd/application.yaml
   ```

### Building Docker Images

```bash
# Frontend
docker build -t ghcr.io/your-org/connections-frontend:latest ./frontend

# Backend
docker build -t ghcr.io/your-org/connections-backend:latest ./backend
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `POST /api/v1/auth/register` | Register new user |
| `POST /api/v1/auth/login` | Login |
| `GET /api/v1/puzzles/today` | Get today's puzzle |
| `POST /api/v1/games` | Start a game |
| `PATCH /api/v1/games/{id}/guess` | Submit a guess |
| `POST /api/v1/ai/hint` | Get AI hint |

## License

MIT
