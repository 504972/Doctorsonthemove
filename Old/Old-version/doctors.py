import sqlite3

# create a connection to the "doctors" database
conn = sqlite3.connect('doctors.db')
c = conn.cursor()

# create a table for doctors with columns for email and password
c.execute('''CREATE TABLE doctors
             (email text UNIQUE, password text)''')

# insert some test data (you can replace this with your actual sign-up process)
c.execute("INSERT INTO doctors VALUES ('director@example.com', 'password1')")
c.execute("INSERT INTO doctors VALUES ('msmith@example.com', 'password2')")
c.execute("INSERT INTO doctors VALUES ('rjohnson@example.com', 'password3')")

# Create a table to store submissions
c.execute('''
    CREATE TABLE submissions (
        id INTEGER PRIMARY KEY,
        company_name TEXT,
        company_mail text UNIQUE,
        region TEXT,
        continent TEXT
    )
''')

# save the changes and close the connection
conn.commit()
conn.close()

conn = sqlite3.connect('doctors.db')
c = conn.cursor()
