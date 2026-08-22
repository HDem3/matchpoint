# MatchPoint

Full-stack tennis matchmaking MVP aligned with Spoat's internship focus: web development, new features, testing/debugging, backend/frontend collaboration and software quality.

## What works

- Responsive React + TypeScript dashboard
- Player registration, match scheduling and score recording
- Match suggestions ranked by city and skill difference
- FastAPI + PostgreSQL API with validation and OpenAPI docs
- Backend API tests and frontend component test

## Local start

```bash
cp .env.example .env
docker compose up --build
```

Open the product at http://localhost:3000 and API docs at http://localhost:8000/docs.

## Tests

```bash
cd backend && pip install -r requirements.txt && pytest -q
cd ../frontend && npm install && npm test && npm run build
```

## Cloud deployment

Deploy three services on Render/Railway/Fly.io: PostgreSQL, `backend` as a Docker web service (port 8000), and `frontend` as a Docker/static service (port 80). Set backend `DATABASE_URL` to the managed PostgreSQL URL. Build the frontend with `VITE_API_URL=https://<backend-domain>` and allow only that frontend origin in production CORS.

For a single VM (Azure, AWS or Hetzner), install Docker and run the compose file behind a TLS reverse proxy. Replace the localhost frontend build argument with the public API domain.

## API highlights

- `POST /players`, `GET /players`
- `GET /players/{id}/suggestions`
- `POST /matches`, `GET /matches`
- `PATCH /matches/{id}/score`

Production follow-ups: authentication, invitations, geospatial distance, ranking/Elo updates, Alembic migrations and end-to-end browser tests.

