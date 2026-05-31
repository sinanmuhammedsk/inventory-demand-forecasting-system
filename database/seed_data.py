import os
import sys
import pandas as pd
import sqlite3

# Ensure the project root is on the import path when this script is run directly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.db_manager import DatabaseManager

def seed():
    print("Starting database seeding...")
    db = DatabaseManager()
    db.init_db()

    # Check if sales_data already has rows
    conn = db.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM sales_data")
        count = cursor.fetchone()[0]
    except Exception as e:
        print(f"Error checking sales_data table: {e}")
        count = 0
    finally:
        conn.close()

    if count > 0:
        print(f"Database already seeded with {count:,} records. Skipping.")
        return

    # Correct relative path to the processed analytical dataset
    processed_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..",
        "dataset",
        "processed",
        "analytical_dataset.csv",
    )
    if os.path.exists(processed_path):
        print(f"Loading processed dataset from {processed_path}...")
        df = pd.read_csv(processed_path)
        df['Date'] = pd.to_datetime(df['Date'])
        db.bulk_insert_sales_data(df)
        print("Database seeding completed successfully.")
    else:
        print("Processed analytical dataset not found. Seeding skipped.")

if __name__ == "__main__":
    seed()
