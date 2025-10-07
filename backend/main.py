import sqlite3
import os
from textblob import TextBlob   # simple AI sentiment analysis

# --- Step 1: Ensure database ---
os.makedirs("data", exist_ok=True)
conn = sqlite3.connect("data/employees.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    department TEXT,
    salary REAL,
    hire_date TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS performance_reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    review_year INTEGER,
    rating REAL,
    comments TEXT,
    FOREIGN KEY(employee_id) REFERENCES employees(id)
)
""")

# Insert sample data only if empty
cursor.execute("SELECT COUNT(*) FROM employees")
if cursor.fetchone()[0] == 0:
    cursor.execute("INSERT INTO employees (name, department, salary, hire_date) VALUES ('Alice', 'Engineering', 70000, '2022-01-15')")
    cursor.execute("INSERT INTO employees (name, department, salary, hire_date) VALUES ('Bob', 'Marketing', 50000, '2021-06-10')")
    cursor.execute("INSERT INTO employees (name, department, salary, hire_date) VALUES ('Charlie', 'HR', 60000, '2023-03-01')")

    cursor.execute("INSERT INTO performance_reviews (employee_id, review_year, rating, comments) VALUES (1, 2023, 4.5, 'Excellent work')")
    cursor.execute("INSERT INTO performance_reviews (employee_id, review_year, rating, comments) VALUES (2, 2023, 4.0, 'Good performance')")
    cursor.execute("INSERT INTO performance_reviews (employee_id, review_year, rating, comments) VALUES (3, 2023, 3.8, 'Satisfactory but needs improvement')")

conn.commit()
conn.close()

# --- Step 2: Fraud Detection ---
def detect_fraud():
    conn = sqlite3.connect("data/employees.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, salary FROM employees WHERE salary < 1000 OR salary > 200000")
    frauds = cursor.fetchall()
    conn.close()
    return frauds

# --- Step 3: AI Documentation Review (Sentiment Analysis) ---
def analyze_reviews():
    conn = sqlite3.connect("data/employees.db")
    cursor = conn.cursor()
    cursor.execute("SELECT e.name, p.comments FROM employees e JOIN performance_reviews p ON e.id = p.employee_id")
    reviews = cursor.fetchall()
    conn.close()

    results = []
    for name, comment in reviews:
        polarity = TextBlob(comment).sentiment.polarity
        if polarity > 0.2:
            sentiment = "Positive"
        elif polarity < -0.2:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        results.append((name, comment, sentiment))
    return results

# --- Step 4: Run Everything ---
print("=== Fraud Detection ===")
frauds = detect_fraud()
if frauds:
    for f in frauds:
        print(f"⚠️ {f[0]} has suspicious salary: {f[1]}")
else:
    print("✅ No fraud detected")

print("\n=== AI Documentation Review (Sentiment Analysis) ===")
reviews = analyze_reviews()
for r in reviews:
    print(f"Employee: {r[0]} | Comment: {r[1]} | Sentiment: {r[2]}")
