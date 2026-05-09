import tkinter as tk
from tkinter import filedialog
import os
import shutil
base_dir = os.path.dirname(os.path.abspath(__file__))
storage_path = os.path.join(base_dir, "Storage Data") # Creates the storage directory if it doesn't already exist
os.makedirs(storage_path, exist_ok=True)
from patient_manager import process_patient_data #function that checks the input
from patient_manager import save_patient_data #function that saves the patient data to a folder
def submit_data():
  name = name_input.get()
  age = age_input.get()
  result = process_patient_data(name, age)
  if isinstance(result, str):
    result_label.config(text=result, fg="red") #Display error message in red
  else:
    name, age, patient_id = result
    save_patient_data(name, age, patient_id)
    result_label.config(text=f"Patient ID: {patient_id}\nName: {name}\nAge: {age}", fg="green") #Display success message in green
def upload_image():
  file_path = tk.filedialog.askopenfilename(
    title="Select Patient X-Ray",
    filetypes=[("Standard Image", "*.jpg *.png"), ("Medical Images", "*.tiff"), ("All Files", "*.*") ]
  )    
app = tk.Tk()
app.title("Dentikonnect")
app.geometry("375x250")
name_input = tk.Entry(app)
name_input.grid(row=0, column=1, padx=20, pady=10, sticky="ew")
name_label = tk.Label(app, text="What is the Patient's Name?:")
name_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
age_input = tk.Entry(app)
age_input.grid(row=1, column=1, padx=20, pady=10, sticky="ew")
age_label = tk.Label(app, text="What is the Patient's Age?:")
age_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
result_label = tk.Label(app, text="", wraplength=400)
result_label.grid(row=2, column=0, columnspan=2, padx=20, pady=10)
upload_button = tk.Button(app, text="Upload X-Ray Image", command=upload_image)
upload_button.grid(row=3, column=0, columnspan=2, pady=10)
submit_button = tk.Button(app, text="Submit", command=submit_data)
submit_button.grid(row=4, column=0, columnspan=2, pady=10)
app.mainloop()