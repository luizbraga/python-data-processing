# Database Seeding

This project includes utilities to seed the database with sample patient data for development and demo purposes.

## Methods

### 1. Automatic Seeding on Startup

Set environment variables in `.env`:

```bash
SEED_DATABASE_ON_STARTUP=True
FORCE_RESEED=False  # Set to True to clear and reseed every time
```

The database will be seeded automatically when the application starts.

**Behavior:**
- `SEED_DATABASE_ON_STARTUP=True`: Seeds only if database is empty
- `FORCE_RESEED=True`: Clears all data and reseeds every time

### 2. Manual Seeding with CLI Script

Run the seeding script manually:

```bash
# Basic seed (only if database is empty)
python scripts/seed_db.py

# Force reseed (clears and reseeds)
python scripts/seed_db.py --force

# Clear data before seeding
python scripts/seed_db.py --clear

# Only clear data (don't seed)
python scripts/seed_db.py --clear-only
```

### 3. Using Alembic Migration

Create a data migration:

```bash
# Create migration from template
cp alembic/versions/seed_sample_data.py.example alembic/versions/001_seed_sample_data.py

# Update the down_revision in the file
# Then run migration
alembic upgrade head

# To remove seed data
alembic downgrade -1
```

## Sample Data

The seeding creates:

**Patients (5):**
- John Doe (Age 40) - Hypertension case
- Jane Smith (Age 35) - Diabetes management
- Robert Johnson (Age 47) - Routine checkup
- Maria Garcia (Age 30) - Prenatal care
- Michael Brown (Age 43) - Post-surgical follow-up

**Notes:** 2-3 clinical notes per patient with realistic medical content

## Usage Recommendations

| Environment | Recommended Method | Settings |
|-------------|-------------------|----------|
| **Development** | Automatic on startup | `SEED_DATABASE_ON_STARTUP=True` |
| **Demo/Staging** | Manual CLI script | Run once with `--force` |
| **Testing** | Test fixtures | Use pytest fixtures |
| **Production** | ⚠️ NEVER | `SEED_DATABASE_ON_STARTUP=False` |

## Safety

⚠️ **Important:**
- Always set `SEED_DATABASE_ON_STARTUP=False` in production
- Seeding checks for existing data and skips unless `force=True`
- Use `--clear-only` to safely remove sample data

## Examples

### Development Setup
```bash
# First time setup
cp .env.example .env
# Edit .env and set SEED_DATABASE_ON_STARTUP=True
uvicorn app.main:app --reload
# Database will be seeded on startup
```

### Demo Environment
```bash
# Reset demo data
python scripts/seed_db.py --force
# Or
FORCE_RESEED=True uvicorn app.main:app
```

### Clean Database
```bash
# Remove all data
python scripts/seed_db.py --clear-only
```
