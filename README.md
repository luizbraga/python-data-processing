# Python Data Processing API

A backend application for managing patient data and clinical notes with AI-powered summary generation.

## Features

### Core Functionality
- **Patient Management** - Full CRUD operations for patient records
- **Clinical Notes** - Create, view, and delete patient notes with file upload support
- **AI-Powered Summaries** - Generate comprehensive patient summaries using LLM (OpenAI)
- **Advanced Search** - Sort and filter patients by various criteria

### Technical Stack
- **FastAPI** - Modern, fast web framework with automatic API documentation
- **SQLAlchemy (Async)** - Asynchronous ORM with connection pooling
- **PostgreSQL** - Production-grade database with full-text search (pg_trgm)
- **Alembic** - Database migration management
- **Pydantic** - Data validation and settings management
- **OpenAI** - LLM integration for clinical summaries

### Quality & Testing
- **pytest** with async support and 90%+ code coverage
- **Black** for consistent code formatting
- **MyPy** for static type checking
- **GitHub Actions** CI/CD with automated testing and coverage reporting

## Setup

### Prerequisites

- Python 3.11 or higher
- PostgreSQL 15 or higher
- Docker and Docker Compose (optional, for containerized deployment)
- OpenAI or Anthropic API key (for AI summary generation)

#### Local Development

1. Clone the repository:
```bash
git clone https://github.com/luizbraga/python-data-processing.git
cd python-data-processing
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create environment file:
```bash
cp .env.example .env
```

Edit `.env` and configure:
- `DATABASE_URL` - PostgreSQL connection string
- `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` - Your LLM provider API key

5. Set up the database:
```bash
# Create database
createdb your_database_name

# Run migrations
alembic upgrade head
```

#### Docker Deployment

1. Clone the repository:
```bash
git clone https://github.com/luizbraga/python-data-processing.git
cd python-data-processing
```

2. Build the Docker image:
```bash
docker build -t python-data-processing .
```

3. Run the container:
```bash
docker run -p 8000:8000 --env-file .env python-data-processing
```

Or with docker-compose:
```bash
docker-compose up
```

The API will be available at `http://localhost:8000`

## Usage

### API Endpoints

#### Patients
- `GET /patients/` - List all patients (with pagination and sorting)
- `GET /patients/{id}` - Get a specific patient
- `POST /patients/` - Create a new patient
- `PUT /patients/{id}` - Update a patient
- `DELETE /patients/{id}` - Delete a patient
- `GET /patients/{id}/summary` - Generate AI-powered patient summary

#### Patient Notes
- `POST /patients/{id}/notes/` - Create a note (JSON body)
- `POST /patients/{id}/notes/upload` - Upload a note from file
- `GET /patients/{id}/notes/` - List all notes for a patient
- `GET /patients/{id}/notes/{note_id}` - Get a specific note
- `DELETE /patients/{id}/notes/{note_id}` - Delete a note
- `DELETE /patients/{id}/notes/` - Delete all notes for a patient

#### Health Check
- `GET /health` - API health status

### Running the Development Server

#### Local
```bash
uvicorn app.main:app --reload
```

#### Docker
```bash
docker-compose up -d
```

The API will be available at `http://localhost:8000`

- API documentation (Swagger UI): `http://localhost:8000/docs`
- Alternative API documentation (ReDoc): `http://localhost:8000/redoc`

### Running Tests

Using Docker environment, you need to enter the bash first and then execute `pytest`
```bash
docker-compose exec app /bin/bash -it
```

```bash
pytest
```

Run with coverage (enforces 90% minimum):
```bash
pytest --cov=app --cov-report=term-missing --cov-fail-under=90 tests/
```

Generate HTML coverage report:
```bash
pytest --cov=app --cov-report=html tests/
open htmlcov/index.html
```

### Code Quality Checks

Format code with Black:
```bash
black app tests
```

Check code formatting:
```bash
black --check app tests
```

Run type checking with MyPy:
```bash
mypy app
```

### Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback migration:
```bash
alembic downgrade -1
```

## Development

### Adding New Dependencies

1. Add the package to `requirements.txt`
2. Install it: `pip install -r requirements.txt`

### Code Style

This project uses:
- **Black** for code formatting (line length: 88)
- **MyPy** for type checking
- Type hints are required for all function signatures

### Continuous Integration

The project uses GitHub Actions to automatically run on every push and pull request:
- **Code formatting** checks with Black
- **Type checking** with MyPy
- **Database migrations** with Alembic
- **Full test suite** with pytest
- **Coverage reporting** to Codecov (90% minimum required)

All checks must pass before merging to main branches.

## Configuration

Environment variables can be set in a `.env` file (see `.env.example`):

### Database Configuration
- `DATABASE_URL` - PostgreSQL connection string (e.g., `postgresql://user:password@localhost:5432/dbname`)

### Application Settings
- `APP_NAME` - Application name (default: `Patient Data Processing`)
- `DEBUG` - Debug mode (default: `false`)

### File Upload Settings
- `MAX_UPLOAD_SIZE` - Maximum file upload size in bytes (default: `10485760` = 10MB)
- `ALLOWED_UPLOAD_TYPES` - Allowed file types (default: `["text/plain"]`)

### LLM Configuration
- `OPENAI_API_KEY` - OpenAI API key (required if using OpenAI)
- `LLM_PROVIDER` - LLM provider to use `openai`
- `LLM_MODEL` - Model name (default: `gpt-4o-mini`)

## Performance Optimization

### AI Summary Generation
The AI summary endpoint can take 3-5 seconds to respond. For better performance:

1. **Use faster models**: Switch to `gpt-4o-mini` instead of `gpt-4`
2. **Enable caching**: Summaries are cached for 1 hour by default
3. **Limit notes**: Only the 50 most recent notes are used for summaries
4. **Streaming** (optional): Implement streaming responses for better UX

### Database Performance
- Connection pooling is enabled by default (10 connections, 20 max overflow)
- PostgreSQL `pg_trgm` extension is used for efficient full-text search
- Async SQLAlchemy provides non-blocking database operations

## Architecture

### Layered Architecture
```
Routes (API Layer)
    ↓
Services (Business Logic)
    ↓
Models (Data Layer)
    ↓
Database
```

### Key Design Patterns
- **Dependency Injection**: Services are injected via FastAPI's `Depends()`
- **Repository Pattern**: Services encapsulate database operations
- **Factory Pattern**: LLM providers use factory pattern for flexibility
- **Async/Await**: Full async support from API to database

## Testing Strategy

- **Unit Tests**: Test individual service methods
- **Integration Tests**: Test API endpoints with real database
- **Mock Tests**: Mock external services (LLM providers)
- **Fixtures**: Reusable test data and database setup
- **Coverage**: Minimum 90% code coverage enforced in CI

## License

See LICENSE file for details.
