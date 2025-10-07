from fastapi import FastAPI, Query
import sqlite3
from backend.schema_discovery import discover_schema

app = FastAPI(title="NLP Query Engine")  # already there

@app.get("/")
def root():
    return {"message": "NLP Query Engine API is running 🚀"}

@app.get("/schema")
def get_schema():
    schema = discover_schema("data/employees.db")
    return {"schema": schema}

# -------------------------------
# NEW ENDPOINT: Natural Language Query
# -------------------------------
@app.get("/query")
def run_query(q: str = Query(..., description="Natural language question")):
    conn = sqlite3.connect("data/employees.db")
    cur = conn.cursor()

    sql = None
    q_lower = q.lower()

    # --- Simple rules (expandable later) ---
    if "all employees" in q_lower:
        sql = "SELECT * FROM employees;"
    elif "highest salary" in q_lower:
        sql = "SELECT name, salary FROM employees ORDER BY salary DESC LIMIT 1;"
    elif "sales department" in q_lower:
        sql = "SELECT name FROM employees WHERE department = 'Sales';"
    elif "average salary" in q_lower:
        sql = "SELECT department, AVG(salary) as avg_salary FROM employees GROUP BY department;"
    elif "performance" in q_lower:
        sql = "SELECT e.name, p.review_year, p.rating FROM employees e JOIN performance_reviews p ON e.id = p.employee_id;"

    # Default fallback
    if not sql:
        return {"error": "Sorry, I don’t understand this query yet."}

    try:
        cur.execute(sql)
        rows = cur.fetchall()
        cols = [description[0] for description in cur.description]
        conn.close()
        return {"query": q, "sql": sql, "results": [dict(zip(cols, row)) for row in rows]}
    except Exception as e:
        return {"error": str(e)}
