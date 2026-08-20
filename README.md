# Rah-e-Ravaan

A modern full-stack application built with React, FastAPI, and PostgreSQL, designed for seamless development using Docker Compose.

## 🚀 Quick Start

### Prerequisites

- Docker Desktop (or Docker Engine + Docker Compose)
- Git
- Make sure Docker is running before starting the stack

### One-Command Startup

```bash
# Clone the repository
git clone <repository-url>
cd rah-e-ravaan

# Copy environment variables
cp .env.example .env

# Start the entire stack
docker-compose up -d
```

That's it! The entire application stack will be available:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📋 Environment Setup

1. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Review and configure environment variables** in `.env`:
   - Database credentials
   - Redis connection
   - Qdrant vector database
   - API keys (OpenAI, Anthropic) - optional for local development

3. **Start the services:**
   ```bash
   docker-compose up -d
   ```

## 🏗️ Architecture

The application consists of the following services:

| Service | Description | Port | Notes |
|---------|-------------|------|-------|
| **web** | React frontend with Vite | 5173 | Hot reload enabled |
| **backend** | FastAPI Python backend | 8000 | Auto-reload enabled |
| **postgres** | PostgreSQL database | 5432 | Persisted data |
| **redis** | Redis cache & message broker | 6379 | Session storage |
| **qdrant** | Vector database for embeddings | 6333 | AI features |

## 🔧 Development Workflow

### Starting the Stack

```bash
# Start all services in detached mode
docker-compose up -d

# Start with live logs
docker-compose up

# Start specific services
docker-compose up web backend
```

### Stopping the Stack

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (deletes data)
docker-compose down -v

# Stop specific service
docker-compose stop backend
```

### Viewing Logs

```bash
# View all logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend

# View last 100 lines
docker-compose logs --tail=100
```

### Rebuilding Services

```bash
# Rebuild and restart specific service
docker-compose up -d --build backend

# Rebuild all services
docker-compose up -d --build

# Force rebuild without cache
docker-compose build --no-cache backend
```

### Database Management

```bash
# Access PostgreSQL container
docker-compose exec postgres psql -U rah_e_ravaan -d rah_e_ravaan

# Access Redis container
docker-compose exec redis redis-cli

# Access Qdrant container
docker-compose exec qdrant curl http://localhost:6333/
```

## 🐛 Troubleshooting

### Port Already in Use

If you see "port already in use" errors:

```bash
# Check what's using the port
netstat -ano | findstr :8000  # Windows
lsof -i :8000                  # Mac/Linux

# Change the port in docker-compose.yml or stop the conflicting service
```

### Database Connection Issues

If the backend can't connect to the database:

1. Ensure all services are running: `docker-compose ps`
2. Check database logs: `docker-compose logs postgres`
3. Verify environment variables in `.env`
4. Try restarting the database: `docker-compose restart postgres`

### Container Won't Start

```bash
# Check container status
docker-compose ps

# View detailed logs
docker-compose logs <service-name>

# Rebuild the container
docker-compose up -d --build <service-name>
``### Volume Issues

If you experience persistent data issues:

```bash
# Stop and remove volumes (WARNING: deletes data)
docker-compose down -v

# Remove specific volume
docker volume rm rah-e-ravaan_postgres_data
```

### Network Issues

If services can't communicate:

```bash
# Restart Docker Desktop
# Or recreate the network
docker-compose down
docker-compose up -d
```

## 📊 Service Endpoints

### Backend API

- **Root**: http://localhost:8000/
- **Health Check**: http://localhost:8000/health
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

### Frontend

- **Application**: http://localhost:5173
- **Vite Dev Server**: http://localhost:5173

### Databases

- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379
- **Qdrant**: http://localhost:6333
- **Qdrant Dashboard**: http://localhost:6333/dashboard

## 🔐 Security Notes

- **Never commit** `.env` files to version control
- **Change default passwords** in production
- **Use strong secret keys** for cryptographic operations
- **Enable HTTPS** in production environments
- **Restrict CORS origins** to your domain only

## 🧪 Testing

### Testing Backend Locally (Without Docker)

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DEBUG=true
export DATABASE_URL=postgresql://user:pass@localhost:5432/db

# Run the server
python -m uvicorn app.main:app --reload
```

### Testing with Docker

```bash
# Run backend tests
docker-compose exec backend pytest

# Run specific test
docker-compose exec backend pytest tests/test_api.py
```

## 📝 Development Notes

- Hot reload is enabled for both frontend and backend
- Database changes persist in Docker volumes
- Redis data persists in Docker volumes
- Qdrant collections persist in Docker volumes
- Changes to code files trigger automatic rebuilds

## 🚦 Production Deployment

For production deployment:

1. Change `DEBUG=false` in `.env`
2. Update `SECRET_KEY` to a strong random value
3. Use environment-specific configuration
4. Enable HTTPS/SSL certificates
5. Configure proper backup strategies
6. Set up monitoring and logging
7. Use docker-compose.prod.yml for production overrides

## 📚 Additional Documentation

- [Backend Documentation](./backend/README.md)
- [Frontend Documentation](./web/README.md)
- [Mobile Documentation](./mobile/README.md)
- [Development Plan](./docs/RER-19-docker-compose-development-plan.md)

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Test with Docker Compose
4. Submit a pull request

## 📄 License

[Your License Here]
