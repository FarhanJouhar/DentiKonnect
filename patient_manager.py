# The python script for handling data input.
"""Decision to move to sqlite3 from the previous folder version
This was due to the need for better data management and scalability as the application grows in scope
sqlite3 was used instead of SQLcypher because it is a built-in library in python, making the application lightweight. 
However, there is a lack of encryption in sqlite3, which will be a concern for future development and will be addressed later"""

import sqlite3
import os
import base64
from datetime import datetime

#The database will be stored inside the following Database folder, which is created if it doesn't exist
def get_db_connection():
    db_dir = "Database"
    os.makedirs(db_dir, exist_ok=True) 
    conn = sqlite3.connect(os.path.join(db_dir, "DentiKonnect.db"))
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

#Creates the patient table if it doesn't exist and patient ID starts from 1000
def create_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT
        )
    """)
    #We create a new visits table to store extra patient details 
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS visits (    
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            visit_date TEXT NOT NULL,
            cc TEXT,
            hpi TEXT,
            pmh TEXT,
            pdh TEXT,       
            ph TEXT,  
            pd TEXT,
            fd TEXT,
            tp TEXT,   
            rx TEXT,                                            
            xray BLOB,
            FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE       
        )
    """)
    cursor.execute("SELECT name FROM sqlite_sequence WHERE name='patients'")
    #The patient ID starts from 1000, so we insert a dummy record with seq 999 to ensure the first real patient gets ID 1000
    if not cursor.fetchone():
        cursor.execute("INSERT INTO sqlite_sequence (name, seq) VALUES ('patients', 999)")
    conn.commit()
    conn.close()

#Saves the patient data to the database, including the name, age, gender, other details and  x-ray image
def save_patient_to_db(name, age, gender):
    # Encrypt everything
    enc_name = encrypt_data(name.encode()) 
    enc_age = encrypt_data(str(age).encode())
    enc_gender = encrypt_data(gender.encode())
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO patients (name, age, gender)
        VALUES (?, ?, ?)
    """, (enc_name, enc_age, enc_gender))
    #Get the ID of the newly inserted patient record
    patient_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return patient_id

def save_visit_to_db(patient_id, cc, hpi, pmh, pdh, ph, pd, fd, tp, Rx, xray_blob):
    visit_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    enc_cc = encrypt_data(cc.encode()) if cc else None
    enc_hpi = encrypt_data(hpi.encode()) if hpi else None
    enc_pmh = encrypt_data(pmh.encode()) if pmh else None
    enc_pdh = encrypt_data(pdh.encode()) if pdh else None
    enc_ph = encrypt_data(ph.encode()) if ph else None
    enc_pd = encrypt_data(pd.encode()) if pd else None
    enc_fd = encrypt_data(fd.encode()) if fd else None
    enc_tp = encrypt_data(tp.encode()) if tp else None
    enc_Rx = encrypt_data(Rx.encode()) if Rx else None
    conn = get_db_connection()
    cursor = conn.cursor() 
    cursor.execute("""
        INSERT INTO visits (patient_id, visit_date, cc, hpi, pmh, pdh, ph, pd, fd, tp, Rx, xray)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (patient_id, visit_date, enc_cc, enc_hpi, enc_pmh, enc_pdh, enc_ph, enc_pd, enc_fd, enc_tp, enc_Rx, xray_blob))
    conn.commit()
    conn.close()
    visit_id = cursor.lastrowid
    return visit_id

#Validates all inputs to make sure they are correct and properly formatted      
def process_patient_data(name, age, gender):
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
  if int(age) <= 0 or int(age) > 120:
    return "Error: Please enter a valid age! (e.g., 25)"
  if gender == "Select Gender":
    return "Error: Please select a valid gender"
  name = name.title()
  return name, age, gender

#We will be trying a simple XOR cipher for encrypting the patient data, which is not the most secure method but serves as a basic example of encryption.
#For this university prototype, a static XOR key is used.
#In a production environment, this would be replaced with AES-256 
#and the key would be managed via an environment variable or Vault.

SECRET_KEY = "THD_DNTIKNKT_ENCR_2026"

def xor_cipher(data, key):
    key_bytes = key.encode()
    # We use a bytearray to perform the XOR math on each byte
    return bytes([data[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(data))])

def encrypt_data(raw_bytes):
    scrambled = xor_cipher(raw_bytes, SECRET_KEY)
    return base64.b64encode(scrambled)

def decrypt_data(encoded_data):
    scrambled = base64.b64decode(encoded_data)
    return xor_cipher(scrambled, SECRET_KEY)

#Function to search for a patient in the database using their name or ID
def search_patient(user_input):
  conn = get_db_connection()
  cursor = conn.cursor()
  cursor.execute("SELECT id, name, age, gender FROM patients")
  rows = cursor.fetchall()
  conn.close()
  filtered_results = []
  for row in rows:
    try:
      p_id = row[0]
      p_name = decrypt_data(row[1]).decode()
      p_age = decrypt_data(row[2]).decode()
      p_gender = decrypt_data(row[3]).decode()
      if user_input.isdigit():
        if int(user_input) == p_id:
          filtered_results.append((p_id, p_name, p_age, p_gender))
      elif user_input in p_name.lower():
          filtered_results.append((p_id, p_name, p_age, p_gender))
    except Exception:
      continue 
  return filtered_results

#Function to upload the x-ray image to the patient's profile after encryption, which is called when the user clicks the "Save X-Ray" button
def save_patient_xray(visit_id, xray_path):
    try:
        with open(xray_path, "rb") as file:
            xray_blob = file.read()
        enc_xray = encrypt_data(xray_blob)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE visits 
            SET xray = ? 
            WHERE id = ?
        """, (enc_xray, visit_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return str(e)
    
#Function to update final diagnosis and treatment plan, from the diagnosis tab
def update_diagnosis(visit_id, fd, tp, rx):
    try:
        enc_fd = encrypt_data(fd.encode())
        enc_tp = encrypt_data(tp.encode())
        enc_rx = encrypt_data(rx.encode())
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE visits 
            SET fd = ?, tp = ?, rx = ?
            WHERE id = ?
        """, (enc_fd, enc_tp, enc_rx, visit_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return str(e)