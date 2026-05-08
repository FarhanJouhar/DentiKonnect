# The python script for handling data input.
import os
STORAGE_PATH = "Storage Data"
ID_FILE = os.path.join(STORAGE_PATH, "patient_id.txt")
#The Storage Data folder is created here, within which the patient_id.txt file exists to permanently store the current ID.
os.makedirs(STORAGE_PATH, exist_ok=True)
if not os.path.exists(ID_FILE):
  with open(ID_FILE, "w") as id_file:
    id_file.write("1000")
#The get_patient_id function reads the current patient ID and increments it by 1 for each use
def get_patient_id():
  with open(ID_FILE, "r") as id_file:
    current_id = int(id_file.read().strip())
  new_id = current_id + 1
  with open(ID_FILE, "w") as id_file:
    id_file.write(str(new_id))
  return new_id
#Checks the patient data for valid input
def process_patient_data(name, age):
  Patient_ID = get_patient_id()
  if not name.strip():
    return "Error: Name cannot be blank" 
  if name.isdigit():
    return "Error: Name cannot be a number (e.g., John Doe)"
  if not all(char.isalpha() or char.isspace() for char in name):
    return "Error: Name must contain only letters and spaces. (e.g., John Doe)"#To prevent weird names like John$ Doe
  if not age.isdigit():
    return "Error: Age must be a number (e.g., 25)"
  if age.startswith("0") and age != "0":
    return "Error: Age cannot start with a zero (e.g., 25, not 025)"
  if int(age) <= 0:
    return "Error: Please enter a valid age! (e.g., 25)"
  name = name.title() #Capitalize the first letter of each word in the name
  return name, age, Patient_ID