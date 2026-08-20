# Rah-e-Ravaan Backend

FastAPI backend for Rah-e-Ravaan application with PostgreSQL, Redis, and Qdrant integration.

## 🚀 Quick Start

### Docker Development (Recommended)

The easiest way to develop the backend is using Docker Compose:

```bash
# From the project root
docker-compose up -d backend

# View logs
docker-compose logs -f backend

# Access the API
curl http://localhost:8000/
```

### Local Development

You can also run the backend locally without Docker:

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp ../.env.example .env

# Set up local database (optional - for testing without Docker)
# Update DATABASE_URL in .env to point to local PostgreSQL

# Run the server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL (for local development)
- Redis (for local development)
- Qdrant (for local development, optional)

Or just Docker for containerized development.

## 🏗️ Project Structure

```
backend/
├── app/
│   ├── api/              # API endpoints
│   ├── core/             # Core functionality
│   │   ├── config.py     # Configuration management
│   │   ├── database.py   # Database connection
│   │   ├── redis.py      # Redis client
│   │   └── qdrant.py     # Qdrant client
│   ├── models/           # Database models
│   ├── services/         # Business logic
│   └── main.py           # FastAPI application
├── tests/                # Test files
├── Dockerfile            # Production Docker image
├── pyproject.toml        # Python dependencies
└── requirements.txt      # Generated requirements
```

## 🔧 Configuration

The backend uses environment variables for configuration. See `.env.example` for all available options:

```bash
# Database
DATABASE_URL=postgresql://rah_e_ravaan:password@postgres:5432/rah_e_ravaan

# Redis
REDIS_URL=redis://redis:6379/0

# Qdrant
QDRANT_URL=http://qdrant:6333
QDRANT_API_KEY=

# Application
DEBUG=true
SECRET_KEY=your-secret-key-here
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

# API Keys (optional)
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
```

## 🧪 Testing

### Running Tests with Docker

```bash
# Run all tests
docker-compose exec backend pytest

# Run with coverage
docker-compose exec backend pytest --cov=app

# Run specific test file
docker-compose exec backend pytest tests/test_api.py
```

### Running Tests Locally

```bash
cd backend

# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run tests
pytest

# Run with coverage
pytest --cov=app
```

## 🐛 Debugging

### Docker Development

```bash
# View backend logs
docker-compose logs -f backend

# Access the container shell
docker-compose exec backend bash

# Check environment variables
docker-compose exec backend env

# Test database connection
docker-compose exec backend python -c "from app.core.database import check_db_health; import asyncio; print(asyncio.run(check_db_health()))"
```

### Local Development

```bash
# Run with debugger
python -m debugpy --listen 5678 -m uvicorn app.main:app --reload

# Set breakpoints in your IDE and connect to localhost:5678

# Check database connection
python -c "from app.core.database import check_db_health; import asyncio; print(asyncio.run(check_db_health()))"
```

## 📊 API Endpoints

### Health Check

```bash
curl http://localhost:8000/health
```

Returns the health status of all services:
- Database connection
- Redis connection  
- Qdrant connection

### API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Configuration Endpoint (Debug Only)

```bash
curl http://localhost:8000/config
```

Returns current configuration (only available when `DEBUG=true`).

## 🔌 Database Operations

### Using Docker Compose

```bash
# Access PostgreSQL
docker-compose exec postgres psql -U rah_e_ravaan -d rah_e_ravaan

# Run SQL commands
SELECT * FROM users;

# Import database dump
docker-compose exec -T postgres psql -U rah_e_ravaan -d rah_e_ravaan < dump.sql

# Export database
docker-compose exec postgres pg_dump -U rah_e_ravaan rah_e_ravaan > backup.sql
```

### Local Development

```bash
# Connect to local PostgreSQL
psql -U rah_e_ravaan -d rah_e_ravaan -h localhost

# Create database
createdb -U rah_e_ravaan rah_e_ravaan
```

## 🚦 Production Considerations

For production deployment:

1. **Security**:
   - Set `DEBUG=false`
   - Use strong `SECRET_KEY`
   - Enable HTTPS
   - Configure proper CORS origins

2. **Database**:
   - Use connection pooling
   - Enable SSL for database connections
   - Set up regular backups
   - Use read replicas for scaling

3. **Performance**:
   - Enable Gunicorn/uvicorn workers
   - Configure proper caching with Redis
   - Use CDN for static assets
   - Enable compression

4. **Monitoring**:
   - Set up application monitoring
   - Configure error tracking (Sentry, etc.)
   - Enable structured logging
   - Set up health check endpoints

## 🛠️ Development Tips

### Hot Reload

Both Docker and local development support hot reload. Changes to Python files will automatically restart the server.

### Database Migrations

If using Alembic for migrations:

```bash
# Generate migration
docker-compose exec backend alembic revision --autogenerate -m "description"

# Apply migration
docker-compose exec backend alembic upgrade head

# Rollback migration
docker-compose exec backend alembic downgrade -1
```

### Redis Operations

```bash
# Access Redis CLI
docker-compose exec redis redis-cli

# Check all keys
KEYS *

# Get value
GET key_name

# Set value
SET key_name "value"

# Flush all data (careful!)
FLUSHALL
```

### Qdrant Operations

```bash
# Check Qdrant status
curl http://localhost:6333/

# List collections
curl http://localhost:6333/collections

# Get collection info
curl http://localhost:6333/collections/{collection_name}
```

## 🐳 Docker vs Local Development

### Docker Development (Recommended)

**Pros:**
- Consistent environment across team
- Easy dependency management
- Built-in database and cache services
- Simple onboarding for new developers
- Reproducible builds

**Cons:**
- Slightly slower startup
- Requires Docker installation
- More resource intensive

### Local Development

**Pros:**
- Faster iteration
- Direct access to local tools
- Easier debugging with IDEs
- Less resource usage

**Cons:**
- Manual dependency setup
- Environment inconsistencies
- Need to set up local databases
- More complex onboarding

## 📝 Code Style

This project follows:
- PEP 8 for Python code
- Type hints for function signatures
- Docstrings for public functions
- Pydantic models for data validation

## 🤝 Contributing

1. Follow the existing code style
2. Add tests for new features
3. Update documentation
4. Test with both Docker and local development
5. Submit pull requests with clear descriptions

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Redis Documentation](https://redis.io/docs/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Docker Documentation](https://docs.docker.com/)
