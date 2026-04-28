# The python script for handling data input.
Patient_ID = 1000
while True:
  patient_name = str(input("Enter the patient's name: "))
  if not patient_name:
    print("Name cannot be blank!") #Names can no longer be blank
    continue
  if patient_name.lower() == "exit": #eXiT can be typed in any way
    break
#Following loop will ensure that only valid integers and positive numbers are accepted into age.
  while True:
    try:
      patient_age = int(input("Enter the patient's age: "))
      if patient_age > 0:
        break
      else:
        print("Please enter a real age!")
    except ValueError: 
      print("Please enter a number!")
  Patient_ID +=1
  print("="*30)
  print(f"Patient ID: {Patient_ID}")
  print(f"Patient Name: {patient_name.title()}")
  print(f"Patient Age: {patient_age}")
  print("="*30)