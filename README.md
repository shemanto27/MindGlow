<div align="center">

# 🧠 MindGlow

**An AI-powered mental wellness backend — built for reflection, learning, and growth.**

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.16-ff1709?logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-10a37f?logo=openai&logoColor=white)](https://openai.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-316192?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![uv](https://img.shields.io/badge/uv-Package%20Manager-DE5FE9)](https://docs.astral.sh/uv/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

**Created by [Shemanto Sharkar](https://github.com/Shemanto27)**

</div>

---

## 📺 Project Demo

<div align="center">

[![MindGlow Demo](https://img.youtube.com/vi/oWQYTgwZuDU/maxresdefault.jpg)](https://www.youtube.com/watch?v=oWQYTgwZuDU)

> 🎬 *Click the thumbnail to watch the full demo on YouTube*

</div>

---

## 📖 Overview

**MindGlow** is a production-ready REST API backend that powers an AI-driven mental wellness platform. It combines **emotionally intelligent chatbots**, **structured learning conversations**, **daily inspirations**, and **reflective journaling** into one cohesive system.

| Feature | Description |
|---|---|
| 🤖 **ReflectBot** | Emotionally supportive, non-directive reflection chatbot with crisis detection |
| 📚 **InnerLearningBot** | Structured educational AI responses with semantic memory |
| 💡 **Daily Inspirations** | AI-curated quotes and motivational content with YouTube search integration |
| 🗒️ **Learnings Journal** | Personal growth tracking and log management |
| 🔒 **Auth System** | JWT-based authentication with social login support |

---

## ⚙️ Tech Stack

### 🐍 Backend Core
| Technology | Version | Purpose |
|---|---|---|
| **Python** | 3.12+ | Runtime |
| **Django** | 6.0 | Web Framework |
| **Django REST Framework** | 3.16 | API Layer |
| **dj-rest-auth + allauth** | Latest | Authentication & Social Login |
| **SimpleJWT** | 5.5 | JWT Token Management |

### 🤖 AI & Intelligence
| Technology | Purpose |
|---|---|
| **OpenAI GPT-4o** | Core language model for both chatbots |
| **text-embedding-3-small** | Semantic similarity and memory ranking |
| **langdetect** | Multi-language detection & response matching |
| **YouTube Data API** | Inspirational video search and recommendation |

### 🗄️ Data & Storage
| Technology | Purpose |
|---|---|
| **PostgreSQL** | Primary relational database |
| **AWS S3 + django-storages** | Media and file storage |
| **boto3** | AWS SDK integration |

### 🚀 Infrastructure & DevOps
| Technology | Purpose |
|---|---|
| **Docker & Docker Compose** | Containerization (dev & prod) |
| **Nginx** | Reverse proxy & static file serving |
| **Gunicorn** | WSGI production server |
| **Terraform** | Infrastructure as Code (AWS) |
| **Ansible** | Server provisioning & configuration |
| **GitHub Actions** | CI/CD Pipeline |
| **Sentry** | Error monitoring & alerting |

### 🛠️ Developer Experience
| Technology | Purpose |
|---|---|
| **uv** | Ultra-fast Python package manager |
| **drf-yasg** | Auto-generated Swagger/ReDoc docs |
| **django-unfold** | Modern, beautiful admin interface |
| **pre-commit + black + isort** | Code quality & formatting |

---

## 📁 Folder Structure

```
MindGlow/
├── 📂 backend/                    # Django application root
│   ├── 📂 ai/                     # AI chatbot engine & utilities
│   │   ├── chatbot_reflect.py     # ReflectBot — emotionally supportive AI
│   │   ├── chatbot_learning.py    # InnerLearningBot — structured learning AI
│   │   ├── config.py              # Settings, prompts, crisis resources
│   │   ├── filters.py             # Language, directive & crisis detection
│   │   ├── memory.py              # Semantic embedding & memory ranking
│   │   ├── youtube_search.py      # YouTube Data API integration
│   │   ├── inspire_quote.py       # AI-generated quote utility
│   │   ├── prompt_loader.py       # Prompt template loader
│   │   └── models.py              # Pydantic models for AI contracts
│   │
│   ├── 📂 apps/                   # Django business logic apps
│   │   ├── users/                 # User registration, profile, JWT auth
│   │   ├── reflections_chat/      # Reflection conversation sessions
│   │   ├── learnings/             # Learning journal & session tracking
│   │   ├── inspirations/          # Daily inspirations & AI quotes
│   │   ├── qoute/                 # Quote management
│   │   ├── app_settings/          # User preferences & app configuration
│   │   └── admin/                 # Extended admin configurations
│   │
│   ├── 📂 core/                   # Django project configuration
│   │   ├── settings.py            # Main settings (env-driven)
│   │   ├── urls.py                # Root URL routing
│   │   ├── wsgi.py                # WSGI entry point
│   │   └── asgi.py                # ASGI entry point
│   │
│   ├── 📂 templates/              # HTML templates (email, admin)
│   ├── 📂 static/                 # Static assets
│   ├── Dockerfile                 # Backend container definition
│   ├── entrypoint.sh              # Container startup script
│   ├── manage.py                  # Django management CLI
│   └── pyproject.toml             # Project dependencies (uv)
│
├── 📂 nginx/                      # Reverse proxy configuration
│   └── backend.conf               # Nginx server block
│
├── 📂 infra/                      # Infrastructure as Code
│   ├── terraform/                 # AWS resource provisioning
│   └── ansible/                   # Server setup & deployment playbooks
│
├── 📂 monitoring/                 # Observability stack
│   └── (Prometheus & Grafana config)
│
├── 📂 .github/
│   └── workflows/                 # GitHub Actions CI/CD pipelines
│
├── docker-compose.dev.yml         # Development environment
├── docker-compose.prod.yml        # Production environment
├── docker-helper.sh               # Docker utility scripts
└── DEVELOPMENT_GUIDE.md           # Detailed local setup instructions
```

---

## 🚀 Quick Start

> 📖 For full step-by-step instructions, see **[DEVELOPMENT_GUIDE.md](./DEVELOPMENT_GUIDE.md)**

### Prerequisites
- Python 3.12+
- [`uv`](https://docs.astral.sh/uv/) installed
- Docker & Docker Compose (recommended)
- PostgreSQL (or use Docker)

### 1. Clone & Set Up Environment
```bash
git clone https://github.com/Shemanto27/MindGlow.git
cd MindGlow/backend

# Install dependencies with uv
uv sync

# Configure environment
cp .env.example .env
# Edit .env with your credentials
```

### 2. Run with Docker (Recommended)
```bash
# Development
docker compose -f docker-compose.dev.yml up --build

# Production
docker compose -f docker-compose.prod.yml up --build
```

### 3. Run Locally
```bash
uv run python manage.py migrate
uv run python manage.py createsuperuser
uv run python manage.py runserver
```

---


## 📡 API Documentation

Once running, visit:

| Endpoint | Description |
|---|---|
| `http://localhost:8000/api/swagger.json/` | Swagger UI |
| `http://localhost:8000/api/docs/` | ReDoc Documentation |
| `http://localhost:8000/admin/` | Django Unfold Admin |
| `http://localhost:8000/api/health-check/` | Health Check |

### Authentication
```
Authorization: Bearer <access_token>

POST /api/token/          → Obtain JWT
POST /api/token/refresh/  → Refresh JWT
```

---

## 🤖 AI Modules

### ReflectBot
An emotionally supportive chatbot that facilitates non-directive reflection:
- Detects user language and responds in-kind
- Filters directive/advice-giving language automatically
- Detects crisis signals and returns localized emergency resources
- Supports option-based conversation deepening

### InnerLearningBot
A structured educational AI companion:
- Delivers clear, layered educational explanations
- Uses semantic embeddings for contextual memory ranking
- Crisis-aware with safe escalation paths

```python
from ai.chatbot_reflect import ReflectBot
from ai.chatbot_learning import InnerLearningBot

reflect = ReflectBot()
response = reflect.chat("I feel overwhelmed today")
print(response["reply"])
```

---

## 🏗️ Architecture

```
Client Request
     │
     ▼
  Nginx (Reverse Proxy)
     │
     ▼
  Gunicorn (WSGI Server)
     │
     ▼
  Django Application
     ├── DRF API Views
     ├── JWT Auth Middleware
     ├── AI Engine (OpenAI GPT-4o)
     └── Business Logic Apps
          │
          ├── PostgreSQL (Primary DB)
          ├── AWS S3 (Media Storage)
          └── OpenAI API (External)
```

---

## 🔒 Security

- ✅ Secrets managed via `.env` — never committed to version control
- ✅ Passwords hashed via Argon2/PBKDF2
- ✅ JWT tokens with refresh rotation
- ✅ CORS headers properly configured
- ✅ Sentry for real-time error monitoring
- ✅ Crisis detection in all AI response paths

---

## 📊 Monitoring

| Tool | Endpoint |
|---|---|
| **Prometheus** | `/metrics/` |
| **Grafana** | Dashboard (configured in `/monitoring/`) |
| **Sentry** | Real-time error tracking |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m 'feat: add your feature'`
4. Push to branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 👨‍💻 Author

**Shemanto Sharkar**
- GitHub: [@Shemanto27](https://github.com/Shemanto27)

---

<div align="center">

Made with ❤️ and ☕ | MindGlow © 2025

</div>