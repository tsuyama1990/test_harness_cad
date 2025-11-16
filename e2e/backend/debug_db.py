
import os
import sys

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import json
import sqlite3

db_path = 'app/test.db'
print("--- Starting DB Debug Script ---")
print(f"Current working directory: {os.getcwd()}")
print(f"Checking for database file at: {os.path.abspath(db_path)}")

if not os.path.exists(db_path):
    print(f"ERROR: Database file not found at '{db_path}'")
    exit()

try:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print(f"\n--- 1. Checking for tables in {db_path} ---")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    if not tables:
        print("RESULT: No tables found in the database.")
    else:
        table_names = [table['name'] for table in tables]
        print("RESULT: Tables found:", table_names)

        if 'harnesses' in table_names:
            print("\n--- 2. Checking content of 'harnesses' table ---")
            cursor.execute("SELECT * FROM harnesses;")
            rows = cursor.fetchall()
            
            if not rows:
                print("RESULT: 'harnesses' table is empty.")
            else:
                print(f"RESULT: {len(rows)} row(s) found in 'harnesses' table:")
                for row in rows:
                    print(json.dumps(dict(row), indent=2))
        else:
            print("\n--- 2. 'harnesses' table not found. ---")

    conn.close()
except Exception as e:
    print(f"\nAn error occurred: {e}")

print("\n--- DB Debug Script Finished ---")
