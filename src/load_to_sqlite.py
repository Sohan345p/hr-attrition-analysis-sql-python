"""
Step 2: Load the CSV into a SQLite database.

Run:  python src/load_to_sqlite.py
Output: hr_attrition.db (in the project root)
"""
import os
import sqlite3
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(ROOT, "data", "employees.csv")
SCHEMA_PATH = os.path.join(ROOT, "sql", "schema.sql")
DB_PATH = os.path.join(ROOT, "hr_attrition.db")


def main():
    df = pd.read_csv(CSV_PATH)

    # Basic data-quality checks before loading
    print("Rows:", len(df))
    print("Missing values:", int(df.isnull().sum().sum()))
    print("Duplicate employee IDs:", int(df["employee_id"].duplicated().sum()))

    conn = sqlite3.connect(DB_PATH)
    with open(SCHEMA_PATH) as f:
        conn.executescript(f.read())          # create the table
    df.to_sql("employees", conn, if_exists="append", index=False)
    count = conn.execute("SELECT COUNT(*) FROM employees").fetchone()[0]
    conn.close()
    print(f"Loaded {count} rows into {DB_PATH}")


if __name__ == "__main__":
    main()
