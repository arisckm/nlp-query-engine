from fastapi import FastAPI, Query
from backend.schema_discovery import discover_schema
import sqlite3, re

app = FastAPI(title="NLP Query Engine")  # <-- crucial

@app.get("/")
def root():
    return {"message": "NLP Query Engine API is running 🚀"}

@app.get("/schema")
def get_schema():
    schema = discover_schema("data/employees.db")
    return {"schema": schema}

@app.post("/query")
def run_query(user_query: str = Query(..., description="Natural language query")):
    conn = sqlite3.connect("data/employees.db")
    cursor = conn.cursor()

    sql = None
    # Basic rules for demo
    if "all employees" in user_query.lower():
        sql = "SELECT * FROM employees;"
    elif "it" in user_query.lower():
        sql = "SELECT * FROM employees WHERE department='IT';"
    elif "salary above" in user_query.lower():
        match = re.search(r"salary above (\d+)", user_query.lower())
        if match:
            amount = match.group(1)
            sql = f"SELECT * FROM employees WHERE salary > {amount};"

    if not sql:
        return {"error": "Query not understood yet."}

    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()

    return {"query": sql, "results": rows}
