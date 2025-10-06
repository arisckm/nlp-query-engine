from fastapi import FastAPI
from backend.schema_discovery import discover_schema

app = FastAPI(title="NLP Query Engine")  # <-- This is crucial

@app.get("/")
def root():
    return {"message": "NLP Query Engine API is running 🚀"}

@app.get("/schema")
def get_schema():
    schema = discover_schema("data/employees.db")
    return {"schema": schema}


