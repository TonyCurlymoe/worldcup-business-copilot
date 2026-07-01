# World Cup Business Intelligence Copilot

A production-oriented AI application for World Cup commercial intelligence. It combines a FastAPI backend, Streamlit frontend, football data integrations, news retrieval, OpenAI-powered analysis, and Plotly dashboards.

## Features

- **Live World Cup Dashboard** with team and match intelligence.
- **Team Business Value Score** combining marketability, reach, sponsorship, form, and rank.
- **AI Match Analysis** for commercial opportunities and risks.
- **Sponsor Impact Analysis** for campaign planning.
- **News Retrieval (RAG-ready)** via News API with demo fallback data.
- **Football Data API** integration with demo fallback data.
- **OpenAI GPT Analysis** with safe demo mode when no key is configured.
- **Plotly Dashboard** embedded in Streamlit.
- **Docker** and Docker Compose for repeatable deployments.
- **GitHub Actions** for linting and testing on Python 3.13.

## Project Structure

```text
src/
  api/          FastAPI application
  app/          Streamlit application
  core/         Configuration
  models/       Pydantic schemas
  services/     OpenAI, news, and football data services
tests/          API tests
data/           Local data and cache location
config/         Streamlit configuration
```

## Quick Start

```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn src.api.main:app --reload
```

In another terminal:

```bash
streamlit run src/app/streamlit_app.py
```

Open the API at <http://localhost:8000/docs> and the app at <http://localhost:8501>.

## Configuration

Copy `.env.example` to `.env` and set optional keys:

- `OPENAI_API_KEY` for GPT analysis.
- `FOOTBALL_DATA_API_KEY` for live World Cup match data.
- `NEWS_API_KEY` for live news retrieval.

Without keys, the application runs in demo mode with deterministic sample data.

## Docker

```bash
cp .env.example .env
docker compose up --build
```

## Quality Checks

```bash
ruff check .
pytest
```

## Production Notes

- Secrets are loaded from environment variables and excluded from git.
- External API calls use explicit timeouts and safe demo fallbacks.
- Pydantic models validate request and response payloads.
- CI runs linting and tests on Python 3.13.
- Streamlit is decoupled from the API through `FRONTEND_API_BASE_URL`.
