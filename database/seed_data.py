import os
import pandas as pd
import sqlite3
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
        
    processed_path = r"d:\forecast\dataset\processed\analytical_dataset.csv"
    if os.path.exists(processed_path):
        print(f"Loading processed dataset from {processed_path}...")
        # Load data
        df = pd.read_csv(processed_path)
        
        # Ensure correct date format
        df['Date'] = pd.to_datetime(df['Date'])
        
        # We can seed a high-quality subset or the entire set.
        # SQLite handles 420k rows easily, but let's seed all of it to provide a production-quality BI experience.
        db.bulk_insert_sales_data(df)
        print("Database seeding completed successfully.")
    else:
        print("Processed analytical dataset not found. Seeding skipped.")

if __name__ == "__main__":
    seed()
