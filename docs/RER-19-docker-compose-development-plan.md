# RER-19: Docker Compose Local Environment Development Plan

## Overview

**Objective**: Enable any developer to bring up the full Rah-e-Ravaan stack with a single command using Docker Compose.

**Scope**: Set up a complete local development environment including PostgreSQL, Redis, Qdrant vector database, and the FastAPI backend service, all orchestrated through Docker Compose.

## Current State Analysis

### Existing Infrastructure
- **Backend**: FastAPI application in `/backend` with basic setup
- **Dependencies**: FastAPI, Uvicorn (defined in `pyproject.toml`)
- **Current Backend Structure**:
  - `/backend/app/main.py` - Basic FastAPI app
  - `/backend/pyproject.toml` - Python dependencies
  - `/backend/app/` - Module structure (api, core, models, services)

### Requirements
- PostgreSQL 16 for relational data
- Redis 7 for caching and message queuing
- Qdrant vector database for embeddings/search
- Backend service with hot-reload for development
- Environment configuration management
- Data persistence across container restarts

## Development Steps

### Phase 1: Backend Dockerfile Creation

**Objective**: Create a multi-stage Dockerfile for the backend service.

**Tasks**:
1. Create `/backend/Dockerfile` with the following stages:
   - **Base stage**: Python 3.11+ slim image
   - **Dependencies stage**: Install system dependencies and Python packages
   - **Development stage**: Copy application code with hot-reload support
   - **Production stage**: Optimized for production builds

2. Key Dockerfile features:
   - Use Python 3.11+ official image
   - Set working directory to `/app`
   - Copy `pyproject.toml` and install dependencies
   - Expose port 8000 for FastAPI
   - Use `uvicorn` with `--reload` flag for development
   - Set environment variables for Python path
   - Health check endpoint configuration

**Acceptance Criteria**:
- Dockerfile builds successfully
- Container can run the FastAPI application
- Hot-reload works in development mode
- All dependencies are properly installed

### Phase 2: Docker Compose Configuration

**Objective**: Create `docker-compose.yml` to orchestrate all services.

**Tasks**:
1. Create `/docker-compose.yml` with the following services:

   **PostgreSQL Service**:
   - Image: `postgres:16`
   - Environment variables for database configuration
   - Named volume for data persistence
   - Port mapping: `5432:5432`
   - Health check for database readiness

   **Redis Service**:
   - Image: `redis:7`
   - Named volume for data persistence
   - Port mapping: `6379:6379`
   - Health check for Redis availability

   **Qdrant Service**:
   - Image: `qdrant/qdrant:latest`
   - Named volume for vector data persistence
   - Port mappings: `6333:6333` (HTTP), `6334:6334` (gRPC)
   - Configuration for embedded mode or standalone

   **Backend Service**:
   - Build from local `./backend` directory
   - Development target from Dockerfile
   - Port mapping: `8000:8000`
   - Environment variables from `.env` file
   - Volume mounts for hot-reload (mount `/app` directory)
   - Depends on postgres, redis, and qdrant services
   - Health check for API availability

   **Optional Web Dev Service**:
   - Build from local `./web` directory
   - Port mapping: `5173:5173` (Vite dev server)
   - Volume mounts for hot-reload
   - Environment variables for API endpoint

2. Define named volumes:
   - `postgres_data` - PostgreSQL data persistence
   - `redis_data` - Redis data persistence
   - `qdrant_data` - Qdrant vector data persistence

3. Configure networking:
   - Create default network for service communication
   - Service discovery using service names

**Acceptance Criteria**:
- All services start with `docker-compose up`
- Services can communicate with each other
- Data persists across container restarts
- Hot-reload works for backend and web services

### Phase 3: Environment Configuration

**Objective**: Create comprehensive environment variable management.

**Tasks**:
1. Create `/.env.example` with all required variables:

   **Database Configuration**:
   ```
   DATABASE_URL=postgresql://rah_e_ravaan:password@postgres:5432/rah_e_ravaan
   POSTGRES_USER=rah_e_ravaan
   POSTGRES_PASSWORD=password
   POSTGRES_DB=rah_e_ravaan
   ```

   **Redis Configuration**:
   ```
   REDIS_URL=redis://redis:6379/0
   ```

   **Qdrant Configuration**:
   ```
   QDRANT_URL=http://qdrant:6333
   QDRANT_API_KEY=
   ```

   **Backend Configuration**:
   ```
   BACKEND_HOST=0.0.0.0
   BACKEND_PORT=8000
   DEBUG=true
   SECRET_KEY=your-secret-key-here
   ```

   **API Keys (placeholder)**:
   ```
   OPENAI_API_KEY=
   ANTHROPIC_API_KEY=
   ```

2. Update backend dependencies in `pyproject.toml`:
   - Add `python-dotenv` for environment loading
   - Add `pydantic-settings` for configuration management
   - Add `psycopg2-binary` for PostgreSQL support
   - Add `redis` for Redis client
   - Add `qdrant-client` for Qdrant integration

3. Create configuration module in backend:
   - `/backend/app/core/config.py` - Pydantic settings class
   - Load from environment variables with defaults
   - Validate configuration at startup

**Acceptance Criteria**:
- `.env.example` contains all required variables
- Backend can load configuration from environment
- Configuration validation works correctly
- Sensitive values are not hardcoded

### Phase 4: Backend Integration

**Objective**: Integrate backend with database and external services.

**Tasks**:
1. Create database connection module:
   - `/backend/app/core/database.py` - PostgreSQL connection setup
   - Use SQLAlchemy or asyncpg for async database operations
   - Connection pooling configuration
   - Health check for database connectivity

2. Create Redis client module:
   - `/backend/app/core/redis.py` - Redis client setup
   - Connection configuration
   - Health check for Redis availability

3. Create Qdrant client module:
   - `/backend/app/core/qdrant.py` - Qdrant client setup
   - Collection management utilities
   - Health check for Qdrant availability

4. Update FastAPI application:
   - Add startup/shutdown event handlers
   - Initialize database connections on startup
   - Create health check endpoint
   - Add dependency injection for services

**Acceptance Criteria**:
- Backend connects to PostgreSQL successfully
- Backend connects to Redis successfully
- Backend connects to Qdrant successfully
- Health check endpoint reports service status

### Phase 5: Documentation

**Objective**: Document the setup and usage of the Docker environment.

**Tasks**:
1. Create root `README.md` with Docker Compose instructions:
   - Prerequisites (Docker, Docker Compose)
   - Quick start guide
   - Environment setup
   - Service endpoints and ports
   - Troubleshooting common issues

2. Update backend README with Docker-specific instructions:
   - Local development vs Docker development
   - Testing without Docker
   - Debugging tips

3. Add development workflow documentation:
   - Starting the stack
   - Stopping the stack
   - Viewing logs
   - Rebuilding services
   - Database migrations (if applicable)

**Acceptance Criteria**:
- Clear instructions for one-command startup
- All service endpoints documented
- Common issues and solutions documented
- Development workflow clearly explained

## Key Files and Modules

### New Files to Create
```
/docker-compose.yml              # Docker Compose configuration
/backend/Dockerfile              # Backend Docker image definition
/.env.example                    # Environment variables template
/backend/app/core/config.py      # Configuration management
/backend/app/core/database.py    # Database connection
/backend/app/core/redis.py       # Redis client
/backend/app/core/qdrant.py      # Qdrant client
/README.md                       # Root documentation (update)
docs/RER-19-docker-compose-development-plan.md  # This document
```

### Files to Modify
```
/backend/pyproject.toml          # Add dependencies
/backend/app/main.py             # Add service initialization
```

## Acceptance Criteria

### Functional Requirements
1. ✅ `docker-compose up` brings up all services (PostgreSQL, Redis, Qdrant, Backend)
2. ✅ All services are reachable on documented ports:
   - PostgreSQL: `localhost:5432`
   - Redis: `localhost:6379`
   - Qdrant HTTP: `localhost:6333`
   - Qdrant gRPC: `localhost:6334`
   - Backend API: `localhost:8000`
3. ✅ Backend service has hot-reload enabled for development
4. ✅ Data persists across container restarts (PostgreSQL, Redis, Qdrant)
5. ✅ Environment variables are properly loaded from `.env` file
6. ✅ Health check endpoints work for all services

### Technical Requirements
1. ✅ Docker Compose configuration follows best practices
2. ✅ Dockerfile uses multi-stage build for optimization
3. ✅ Named volumes are properly configured for data persistence
4. ✅ Service dependencies are correctly defined
5. ✅ Network configuration allows inter-service communication
6. ✅ Configuration management uses Pydantic settings

### Documentation Requirements
1. ✅ Root README contains one-command startup instructions
2. ✅ `.env.example` contains all required variables with descriptions
3. ✅ Service endpoints and ports are documented
4. ✅ Troubleshooting guide covers common issues

## Testing and Verification

### Manual Testing Steps
1. **Environment Setup**:
   ```bash
   cp .env.example .env
   # Edit .env with appropriate values
   ```

2. **Start Services**:
   ```bash
   docker-compose up -d
   ```

3. **Verify Services**:
   - Check PostgreSQL: `docker-compose exec postgres psql -U rah_e_ravaan -d rah_e_ravaan`
   - Check Redis: `docker-compose exec redis redis-cli ping`
   - Check Qdrant: `curl http://localhost:6333/`
   - Check Backend: `curl http://localhost:8000/health`

4. **Test Hot Reload**:
   - Modify a backend file
   - Verify changes are reflected without restart

5. **Test Data Persistence**:
   - Stop containers: `docker-compose down`
   - Start containers: `docker-compose up -d`
   - Verify data is still present

6. **Clean Up**:
   ```bash
   docker-compose down -v  # Remove volumes to clean data
   ```

### Automated Testing (Future Enhancement)
- Add health check tests to CI/CD pipeline
- Add integration tests for service connectivity
- Add smoke tests for basic functionality

## Technical Considerations

### Security
- Use strong default passwords in `.env.example`
- Document security best practices
- Ensure sensitive data is not committed to git
- Use secrets management for production deployment

### Performance
- Configure appropriate resource limits for containers
- Optimize database connection pooling
- Configure Redis memory limits
- Use appropriate Qdrant storage settings

### Development Experience
- Fast startup times for development
- Clear error messages for common issues
- Easy debugging with volume mounts
- Log aggregation and viewing

### Cross-Platform Compatibility
- Test on Windows, macOS, and Linux
- Handle line ending differences
- Consider platform-specific networking issues
- Document platform-specific requirements

## Timeline Estimate

- **Phase 1 (Dockerfile)**: 2-3 hours
- **Phase 2 (Docker Compose)**: 3-4 hours
- **Phase 3 (Environment Config)**: 2-3 hours
- **Phase 4 (Backend Integration)**: 4-6 hours
- **Phase 5 (Documentation)**: 2-3 hours
- **Testing and Refinement**: 2-3 hours

**Total Estimated Time**: 13-19 hours

## Dependencies and Prerequisites

### External Dependencies
- Docker Desktop or Docker Engine
- Docker Compose v2+
- Git (for cloning repository)

### Internal Dependencies
- Backend service must be functional
- Database schema (if applicable)
- API endpoints (for health checks)

## Risks and Mitigation

### Risk 1: Networking Issues
**Mitigation**: Use service names for inter-service communication, document port mappings clearly

### Risk 2: Data Loss
**Mitigation**: Use named volumes, document backup procedures, test persistence thoroughly

### Risk 3: Environment Variable Conflicts
**Mitigation**: Use `.env.example` as template, validate configuration at startup

### Risk 4: Performance Issues
**Mitigation**: Configure resource limits, monitor container resources, optimize database queries

## Success Metrics

1. Developer can start full stack with single command
2. All services start within 2 minutes
3. Hot-reload works within 5 seconds of file changes
4. Data persists correctly across restarts
5. New developers can set up environment in under 15 minutes

## Next Steps After Completion

1. Add database migration support (Alembic)
2. Add development seed data scripts
3. Create production Docker Compose configuration
4. Add monitoring and logging (Prometheus, Grafana)
5. Create deployment documentation for production

## References

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Docker Deployment](https://fastapi.tiangolo.com/deployment/docker/)
- [PostgreSQL Docker Image](https://hub.docker.com/_/postgres)
- [Redis Docker Image](https://hub.docker.com/_/redis)
- [Qdrant Docker Image](https://hub.docker.com/r/qdrant/qdrant)
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)

---

**Document Version**: 1.0
**Last Updated**: 2026-08-18
**Author**: Development Team
**Status**: Planning Phase
