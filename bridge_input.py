# The python script for handling data input.
Patient_ID = 1000 #tokens start from 1000
def process_patient_data(name, age):
  global Patient_ID
  if not name.strip():
    return "Error: Name cannot be blank" #Names can no longer be blank
  if not age.isdigit():
    return "Error: Age must be a number (e.g., 25)"
  name = name.title() #Capitalize the first letter of each word in the name
  Patient_ID +=1
  return name, age, Patient_ID