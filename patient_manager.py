# The python script for handling data input.
Patient_ID = 1000 #tokens start from 1000
def process_patient_data(name, age):
  global Patient_ID
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
  Patient_ID +=1
  return name, age, Patient_ID