import sqlite3

def discover_schema(db_path="data/employees.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    schema = {}
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for (table_name,) in tables:
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        schema[table_name] = [col[1] for col in columns]

    conn.close()
    return schema

if __name__ == "__main__":
    schema = discover_schema()
    print("Discovered Schema:")
    for table, cols in schema.items():
        print(f"{table}: {cols}")
