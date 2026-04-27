# The python script for handling data input.
while True:
  patient_name = str(input("Enter the patient's name: "))
  if patient_name == "exit":
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
  print("="*30)
  print(f"Patient Name: {patient_name}")
  print(f"Patient Age: {patient_age}")
  print("="*30)