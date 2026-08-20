# Development Workflow Guide

This guide covers the day-to-day development workflow for the Rah-e-Ravaan project using Docker Compose.

## 🚀 Daily Development Setup

### Starting Your Development Day

```bash
# Navigate to project directory
cd rah-e-ravaan

# Start the entire stack
docker-compose up -d

# Verify all services are running
docker-compose ps

# Check service health
curl http://localhost:8000/health
```

### Checking Service Status

```bash
# View all container status
docker-compose ps

# View resource usage
docker stats

# Check specific service logs
docker-compose logs backend
```

## 🔄 Making Code Changes

### Backend Changes

1. **Make changes to backend code**
2. **Hot reload automatically restarts the server**
3. **Test changes at http://localhost:8000**
4. **View logs if needed**: `docker-compose logs -f backend`

### Frontend Changes

1. **Make changes to frontend code**
2. **Vite hot reload automatically updates the browser**
3. **Test changes at http://localhost:5173**
4. **View logs if needed**: `docker-compose logs -f web`

### Database Schema Changes

```bash
# Access PostgreSQL
docker-compose exec postgres psql -U rah_e_ravaan -d rah_e_ravaan

# Make schema changes
CREATE TABLE example_table (...);

# Update backend models accordingly
# Test the changes
```

## 🧪 Testing Workflow

### Running Tests

```bash
# Run backend tests
docker-compose exec backend pytest

# Run with coverage
docker-compose exec backend pytest --cov=app

# Run specific test
docker-compose exec backend pytest tests/test_specific.py
```

### Integration Testing

```bash
# Test API endpoints
curl http://localhost:8000/api/endpoint

# Test database connectivity
docker-compose exec backend python -c "from app.core.database import check_db_health; import asyncio; print(asyncio.run(check_db_health()))"

# Test Redis connectivity
docker-compose exec backend python -c "from app.core.redis import check_redis_health; import asyncio; print(asyncio.run(check_redis_health()))"
```

## 🐛 Debugging Workflow

### Viewing Logs

```bash
# Follow all logs
docker-compose logs -f

# Follow specific service logs
docker-compose logs -f backend
docker-compose logs -f web
docker-compose logs -f postgres

# View last 100 lines
docker-compose logs --tail=100 backend
```

### Accessing Container Shells

```bash
# Access backend container
docker-compose exec backend bash

# Access database container
docker-compose exec postgres bash

# Access Redis container
docker-compose exec redis sh

# Access Qdrant container
docker-compose exec qdrant sh
```

### Common Debugging Scenarios

#### Backend Not Starting

```bash
# Check backend logs
docker-compose logs backend

# Check if dependencies are installed
docker-compose exec backend pip list

# Restart backend
docker-compose restart backend

# Rebuild backend
docker-compose up -d --build backend
```

#### Database Connection Issues

```bash
# Check database logs
docker-compose logs postgres

# Test database connection
docker-compose exec postgres psql -U rah_e_ravaan -d rah_e_ravaan -c "SELECT 1"

# Restart database
docker-compose restart postgres

# Check network connectivity
docker-compose exec backend ping postgres
```

#### Frontend Not Updating

```bash
# Check frontend logs
docker-compose logs web

# Clear browser cache
# Restart frontend
docker-compose restart web

# Rebuild frontend
docker-compose up -d --build web
```

## 📊 Database Management

### Backup and Restore

```bash
# Backup database
docker-compose exec postgres pg_dump -U rah_e_ravaan rah_e_ravaan > backup.sql

# Restore database
docker-compose exec -T postgres psql -U rah_e_ravaan -d rah_e_ravaan < backup.sql

# Backup specific table
docker-compose exec postgres pg_dump -U rah_e_ravaan -t table_name rah_e_ravaan > table_backup.sql
```

### Data Management

```bash
# Access database
docker-compose exec postgres psql -U rah_e_ravaan -d rah_e_ravaan

# List all tables
\dt

# Describe table structure
\d table_name

# Run queries
SELECT * FROM table_name LIMIT 10;

# Exit
\q
```

### Redis Data Management

```bash
# Access Redis
docker-compose exec redis redis-cli

# View all keys
KEYS *

# Get specific key
GET key_name

# Delete key
DEL key_name

# Flush all data (careful!)
FLUSHALL

# Exit
exit
```

## 🔄 Service Management

### Restarting Services

```bash
# Restart specific service
docker-compose restart backend

# Restart all services
docker-compose restart

# Restart with rebuild
docker-compose up -d --build backend
```

### Stopping and Starting

```bash
# Stop all services
docker-compose stop

# Start all services
docker-compose start

# Stop specific service
docker-compose stop backend

# Start specific service
docker-compose start backend
```

### Rebuilding Services

```bash
# Rebuild backend
docker-compose up -d --build backend

# Rebuild all services
docker-compose up -d --build

# Force rebuild without cache
docker-compose build --no-cache backend
docker-compose up -d backend
```

## 🧹 Cleanup Operations

### Regular Cleanup

```bash
# Remove stopped containers
docker container prune

# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# Remove unused networks
docker network prune
```

### Full Cleanup (WARNING: Deletes Data)

```bash
# Stop and remove all containers, networks, and volumes
docker-compose down -v

# Remove all Docker data (careful!)
docker system prune -a --volumes
```

## 📈 Performance Monitoring

### Resource Usage

```bash
# View real-time resource usage
docker stats

# View specific container stats
docker stats backend web postgres redis qdrant
```

### Application Performance

```bash
# Check response times
time curl http://localhost:8000/api/endpoint

# Monitor API performance
docker-compose logs -f backend | grep "GET"
```

## 🔧 Configuration Changes

### Updating Environment Variables

```bash
# Edit .env file
nano .env

# Restart affected services
docker-compose restart backend

# Or restart all services
docker-compose restart
```

### Updating Dependencies

```bash
# Backend dependencies
# Edit pyproject.toml
docker-compose up -d --build backend

# Frontend dependencies
# Edit package.json
docker-compose up -d --build web
```

## 🚢 Deployment Preparation

### Pre-Deployment Checklist

```bash
# Set production environment variables
export DEBUG=false
export SECRET_KEY=<strong-random-key>

# Update CORS origins
export CORS_ORIGINS=https://yourdomain.com

# Test production build
docker-compose -f docker-compose.prod.yml up -d --build

# Run health checks
curl https://your-domain.com/health

# Check logs
docker-compose -f docker-compose.prod.yml logs -f
```

### Database Migration

```bash
# Backup production database
docker-compose exec postgres pg_dump -U rah_e_ravaan rah_e_ravaan > production_backup.sql

# Run migrations
docker-compose exec backend alembic upgrade head

# Verify migration
docker-compose exec postgres psql -U rah_e_ravaan -d rah_e_ravaan -c "\dt"
```

## 🤝 Team Collaboration

### Onboarding New Developers

```bash
# Clone repository
git clone <repository-url>
cd rah-e-ravaan

# Copy environment file
cp .env.example .env

# Start development environment
docker-compose up -d

# Verify setup
curl http://localhost:8000/health
curl http://localhost:5173
```

### Code Review Workflow

1. **Create feature branch**
2. **Make changes and test locally**
3. **Run all tests**: `docker-compose exec backend pytest`
4. **Check code style**
5. **Submit pull request**
6. **Team reviews and tests in Docker environment**
7. **Merge to main**

## 📝 Common Issues and Solutions

### Port Conflicts

**Problem**: Port already in use error

**Solution**:
```bash
# Find what's using the port
netstat -ano | findstr :8000  # Windows
lsof -i :8000                  # Mac/Linux

# Kill the process or change port in docker-compose.yml
```

### Out of Memory

**Problem**: Docker containers running out of memory

**Solution**:
```bash
# Increase Docker memory allocation in Docker Desktop settings
# Or reduce container resource limits in docker-compose.yml
```

### Network Issues

**Problem**: Services can't communicate

**Solution**:
```bash
# Restart Docker Desktop
# Or recreate network
docker-compose down
docker-compose up -d
```

### Permission Issues

**Problem**: File permission errors in containers

**Solution**:
```bash
# On Linux/Mac, adjust file permissions
sudo chown -R $USER:$USER .

# Or use Docker Desktop with proper file sharing settings
```

## 📚 Additional Resources

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Redis Documentation](https://redis.io/docs/)
