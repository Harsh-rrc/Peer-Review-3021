import os
import pymysql
from urllib.request import urlopen
import smtplib
from email.message import EmailMessage

# Sensitive information is written in plain text which can cause sensitive data exposure
# Abstraction method can be used to hide sensitive information
# OWASP A02:2021 - Cryptographic Failures
db_config = {
    'host': os.getenv('DB_HOST', 'mydatabase.com'),
    'user': os.getenv('DB_USER', 'admin'),
    'password': os.getenv('DB_PASS', 'secret123')
}

def get_user_input():
    user_input = input('Enter your name: ')
    return user_input

# using os.system to send email can lead to command injection vulnerabilities
# we can use third party libraries to send email securely
# OWASP A03:2021 - Injection (Command Injection)
def send_email(to, subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = 'admin@example.com'
    msg['To'] = to

    try:
        with smtplib.SMTP('localhost') as server:
            server.send_message(msg)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

# Using HTTP instead of HTTPS can lead to data interception
# We should use HTTPS to ensure data is encrypted during transmission
# OWASP A02:2021 - Cryptographic Failures (Insecure Transport)
def get_data():
    url = 'https://secure-api.com/get-data'
    data = urlopen(url).read().decode()
    return data

# SQL query is constructed using string formatting which can lead to SQL injection vulnerabilities
# We should use parameterized queries to prevent SQL injection
# OWASP A03:2021 - Injection (SQL Injection)
def save_to_db(data):
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    query = "INSERT INTO mytable (column1, column2) VALUES (%s, %s)"
    cursor.execute(query, (data, 'Another Value'))
    connection.commit()
    cursor.close()
    connection.close()
    print("Data saved successfully.")

if __name__ == '__main__':
    user_input = get_user_input()
    data = get_data()
    save_to_db(data)
    send_email('admin@example.com', 'User Input', user_input)
