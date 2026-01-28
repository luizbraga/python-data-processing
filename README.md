# Python Data Processing API

Backend application that processes data using modern API development practices with FastAPI.

## Features

- **FastAPI** framework for building APIs
- **SQLAlchemy** ORM for database operations
- **Alembic** for database migrations
- **Pydantic** for data validation and settings management
- **pytest** for testing
- **Black** for code formatting
- **MyPy** for static type checking
- **GitHub Actions** CI/CD for code quality checks

## Project Structure

```
├── app/                   # Application source code
│   ├── __init__.py
│   ├── main.py            # FastAPI application and routes
│   ├── config.py          # Application settings
│   ├── core/              # Core functionality
│   ├── models/            # SQLAlchemy models
│   ├── routes/            # API route handlers
│   └── schemas/           # Pydantic schemas
├── tests/                 # Test files
│   ├── __init__.py
│   ├── conftest.py        # Test fixtures
│   └── test_main.py       # API tests
├── alembic/               # Database migrations
│   ├── versions/          # Migration scripts
│   ├── env.py             # Alembic environment
│   └── script.py.mako     # Migration template
├── .vscode/               # VS Code settings
│   └── settings.json
├── Dockerfile             # Docker container configuration
├── docker-compose.yml     # Docker Compose orchestration
├── requirements.txt       # Python dependencies
├── pyproject.toml         # Tool configurations
├── alembic.ini            # Alembic configuration
├── .env.example           # Example environment variables
├── .env                   # Environment variables (not in git)
├── test.db                # SQLite database (development)
├── LICENSE                # License file
└── README.md 
```

## Setup

### Prerequisites

- Python 3.11 or higher
- pip
- Docker and Docker Compose (optional, for containerized deployment)

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

5. Initialize the database (optional - tables are created automatically):
```bash
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

### Running the Development Server

#### Local
```bash
uvicorn app.main:app --reload
```

#### Docker
```bash
docker run -p 8000:8000 python-data-processing
```

The API will be available at `http://localhost:8000`

- API documentation (Swagger UI): `http://localhost:8000/docs`
- Alternative API documentation (ReDoc): `http://localhost:8000/redoc`

### Running Tests

```bash
pytest
```

Run with coverage:
```bash
pytest --cov=app tests/
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

The project uses GitHub Actions to automatically run:
- Black formatting checks
- MyPy type checks

These checks run on every push and pull request to `main`, `master`, and `develop` branches.

## Configuration

Environment variables can be set in a `.env` file (see `.env.example`):

- `DATABASE_URL` - Database connection string (default: `sqlite:///./test.db`)
- `APP_NAME` - Application name
- `DEBUG` - Debug mode (default: `False`)

## License

See LICENSE file for details.
