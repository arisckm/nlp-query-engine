import sqlite3

def create_employee_db():
    conn = sqlite3.connect("data/employees.db")
    cursor = conn.cursor()

    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
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
        rating TEXT,
        comments TEXT,
        FOREIGN KEY (employee_id) REFERENCES employees(id)
    )
    """)

    # Insert sample employees
    employees = [
        ("Ayesha Khan", "HR", 70000, "2020-05-15"),
        ("Ali Raza", "Sales", 85000, "2019-03-20"),
        ("Sara Ahmed", "Engineering", 95000, "2021-07-01"),
        ("Hamza Malik", "Finance", 60000, "2022-01-10"),
    ]
    cursor.executemany("INSERT INTO employees (name, department, salary, hire_date) VALUES (?, ?, ?, ?)", employees)

    # Insert sample performance reviews
    reviews = [
        (1, 2023, "Excellent", "Great leadership in HR"),
        (2, 2023, "Good", "Met sales targets"),
        (3, 2023, "Outstanding", "Led key project"),
        (4, 2023, "Average", "Needs improvement in reporting"),
    ]
    cursor.executemany("INSERT INTO performance_reviews (employee_id, review_year, rating, comments) VALUES (?, ?, ?, ?)", reviews)

    conn.commit()
    conn.close()
    print("Database created at data/employees.db")

if __name__ == "__main__":
    create_employee_db()

