import os
import sqlite3
import requests


# 1. OWASP Cryptographic Failures
# Hardcoded credentials (should be in environment variables or a secrets manager)

DB_USERNAME = "admin"
DB_PASSWORD = "password123"
DB_NAME = "users.db"

# Connect to database (not secure way)
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()


# 2. OWASP Injection (SQL Injection)
# Unsafe string formatting used in SQL query

def get_user(username):
    # Vulnerable: directly inserting user input into the query
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)  # attacker can inject malicious SQL
    return cursor.fetchall()


# 3. OWASP Injection (Command Injection)
# Using os.system() with user input

def send_email(recipient_email):
    # Vulnerable: user input directly passed to a system command
    os.system(f"echo 'Hello {recipient_email}' | mail -s 'Test' {recipient_email}")
    # attacker could inject something like: test@example.com; rm -rf /


# 4. OWASP Cryptographic Failures
# Fetching data using insecure HTTP connection

def fetch_data_from_api():
    # Vulnerable: using plain HTTP (data can be intercepted)
    response = requests.get("http://example.com/api/data")
    return response.text


# 5. OWASP Security Misconfiguration
# No input validation for user-provided data

def register_user(username, age):
    # Vulnerable: no checks for username length, content, or age validity
    query = f"INSERT INTO users (username, age) VALUES ('{username}', {age})"
    cursor.execute(query)
    conn.commit()
    print("User registered successfully!")

# Simulate user inputs (for demo)

if __name__ == "__main__":
    # Example user input (imagine these come from a web form)
    username = input("Enter your username: ")
    age = input("Enter your age: ")
    email = input("Enter your email: ")

    get_user(username)
    send_email(email)
    fetch_data_from_api()
    register_user(username, age)