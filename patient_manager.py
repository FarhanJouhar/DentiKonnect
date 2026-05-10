# The python script for handling data input.
"""Decision to move to sqlite3 from the previous folder version
This was due to the need for better data management and scalability as the application grows in scope
sqlite3 was used instead of SQLcypher because it is a built-in library in python, making the application lightweight. 
However, there is a lack of encryption in sqlite3, which will be a concern for future development and will be addressed later"""
import sqlite3
import os

#The database will be stored inside the following Database folder, which is created if it doesn't exist
def get_db_connection():
    db_dir = "Database"
    os.makedirs(db_dir, exist_ok=True) 
    return sqlite3.connect(os.path.join(db_dir, "DentiKonnect.db"))

#Creates the patient table if it doesn't exist and patient ID starts from 1000
def create_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            xray BLOB
        )
    """)
    cursor.execute("SELECT name FROM sqlite_sequence WHERE name='patients'")
    #The patient ID starts from 1000, so we insert a dummy record with seq 999 to ensure the first real patient gets ID 1000
    if not cursor.fetchone():
        cursor.execute("INSERT INTO sqlite_sequence (name, seq) VALUES ('patients', 999)")
    conn.commit()
    conn.close()

#Saves the patient data to the database, including the name, age, and x-ray image
def save_patient_to_db(name, age, xray_blob):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO patients (name, age, xray)
        VALUES (?, ?, ?)
    """, (name, int(age), xray_blob))
    #Get the ID of the newly inserted patient record
    patient_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return patient_id

#Validates all inputs to make sure they are correct and properly formatted      
def process_patient_data(name, age):
  if not name.strip():
    return "Error: Name cannot be blank" 
  if name.isdigit():
    return "Error: Name cannot be a number (e.g., John Doe)"
  if not all(char.isalpha() or char.isspace() for char in name):
    return "Error: Name must contain only letters and spaces. (e.g., John Doe)"
  if not age.isdigit():
    return "Error: Age must be a number (e.g., 25)"
  if age.startswith("0") and age != "0":
    return "Error: Age cannot start with a zero (e.g., 25, not 025)"
  if int(age) <= 0:
    return "Error: Please enter a valid age! (e.g., 25)"
  name = name.title()
  return name, age