from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from backend.schema_discovery import discover_schema
from openai import OpenAI
import os

app = FastAPI(title="NLP Query Engine")

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ✅ Data model for input
class QueryRequest(BaseModel):
    question: str

@app.get("/")
def root():
    return {"message": "NLP Query Engine API is running 🚀"}

@app.get("/schema")
def get_schema():
    schema = discover_schema("data/employees.db")
    return {"schema": schema}

@app.post("/query")
def run_query(req: QueryRequest):
    schema = discover_schema("data/employees.db")

    # Prompt to LLM
    prompt = f"""
    You are an expert in SQL.
    Database schema: {schema}
    Question: {req.question}
    Write a correct SQLite query.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    sql_query = response.choices[0].message.content.strip()

    # ✅ Run SQL safely
    try:
        conn = sqlite3.connect("data/employees.db")
        cursor = conn.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        conn.close()

        results = [dict(zip(columns, row)) for row in rows]
        return {"sql": sql_query, "results": results}

    except Exception as e:
        return {"error": str(e), "sql": sql_query}

