
# Models Documentation

## Adding a New Model

### 1. Create the Model Class

Create a new file in the `app/models/` directory:

```python
from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base

class YourModel(Base):
    __tablename__ = "your_table_name"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
```

### 2. Import the Model

Add your model to `app/models/__init__.py`:

```python
from .your_model import YourModel
```

### 3. Generate Migration

Run Alembic to create a migration:

```bash
alembic revision --autogenerate -m "Add YourModel table"
```

### 4. Review Migration File

Check the generated file in `alembic/versions/`:

- Verify table name is correct
- Check column types and constraints
- Ensure foreign keys are properly defined
- Review indexes

### 5. Apply Migration

```bash
alembic upgrade head
```

### 6. Verify Migration

**Check migration status:**
```bash
alembic current
```

**Check database:**
```bash
# PostgreSQL
psql -d your_database -c "\dt"
psql -d your_database -c "\d your_table_name"

# MySQL
mysql -e "SHOW TABLES;" your_database
mysql -e "DESCRIBE your_table_name;" your_database
```

**Rollback if needed:**
```bash
alembic downgrade -1
```
