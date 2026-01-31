#!/usr/bin/env python
"""CLI script to seed the database with sample data."""

import asyncio
import sys

from app.config import settings
from app.core.db import postgres_db
from app.core.seed import clear_database, seed_database


async def main() -> None:
    """Main function to seed database."""
    import argparse

    parser = argparse.ArgumentParser(description="Database seeding utility")
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Clear all data before seeding",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force reseed even if data exists",
    )
    parser.add_argument(
        "--clear-only",
        action="store_true",
        help="Only clear data, don't seed",
    )

    args = parser.parse_args()

    # Initialize database connection
    await postgres_db.init(settings.database_url)

    try:
        if postgres_db.AsyncSessionLocal is None:
            raise RuntimeError("Database session is not initialized.")
        async with postgres_db.AsyncSessionLocal() as session:
            if args.clear or args.clear_only:
                await clear_database(session)
                if args.clear_only:
                    print("✓ Database cleared successfully!")
                    return

            await seed_database(session, force=args.force)
            print("✓ Database seeded successfully!")

    except Exception as e:
        print(f"✗ Error seeding database: {e}", file=sys.stderr)
        sys.exit(1)

    finally:
        await postgres_db.close()


if __name__ == "__main__":
    asyncio.run(main())
