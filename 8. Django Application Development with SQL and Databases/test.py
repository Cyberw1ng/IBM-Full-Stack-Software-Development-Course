import sqlite3

# Connect to SQLite database (creates a new database if not exists)
conn = sqlite3.connect('example.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Create a table
cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)''')

# Insert data into the table
cursor.execute("INSERT INTO users (name, email) VALUES ('John Doe', 'john@example.com')")
cursor.execute("INSERT INTO users (name, email) VALUES ('Jane Smith', 'jane@example.com')")

# Commit changes to the database
conn.commit()

# Fetch and display data from the table
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
print(rows)

# Close cursor and connection
cursor.close()
conn.close()
