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
├── app/                    # Application source code
│   ├── __init__.py
│   ├── main.py            # FastAPI application and routes
│   ├── config.py          # Application settings
│   ├── database.py        # Database configuration
│   └── models.py          # SQLAlchemy models
├── tests/                 # Test files
│   ├── __init__.py
│   ├── conftest.py        # Test fixtures
│   └── test_main.py       # API tests
├── alembic/               # Database migrations
│   ├── versions/          # Migration scripts
│   └── env.py            # Alembic environment
├── .github/workflows/     # CI/CD workflows
│   └── code-quality.yml   # Black and MyPy checks
├── requirements.txt       # Python dependencies
├── pyproject.toml        # Tool configurations
├── alembic.ini           # Alembic configuration
└── .env.example          # Example environment variables
```

## Setup

### Prerequisites

- Python 3.11 or higher
- pip

### Installation

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

## Usage

### Running the Development Server

```bash
uvicorn app.main:app --reload
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

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check endpoint
- `GET /items` - Get all items
- `POST /items` - Create a new item

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
