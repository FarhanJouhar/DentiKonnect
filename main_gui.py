import tkinter as tk
from tkinter import filedialog
from patient_manager import process_patient_data, save_patient_to_db, create_db, search_patient
create_db()

#Function to upload the xray image
def upload_image():
    global current_xray_path
    path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
    if path:
        current_xray_path = path
        upload_button.config(text="Image Selected", fg="blue")

#Function to submit the data after going through process_patient_data for validation and then to database using save_patient_to_db
def submit_data():
  name = name_input.get()
  age = age_input.get()
  result = process_patient_data(name, age)
  if isinstance(result, str):
    result_label.config(text=result, fg="red")
  else:
    clean_name, clean_age = result
    xray_blob = None
    if 'current_xray_path' in globals() and current_xray_path:
      with open(current_xray_path, "rb") as file:
        xray_blob = file.read()
    new_id = save_patient_to_db(clean_name, clean_age, xray_blob)
    result_label.config(text=f"Success!\nPatient Name: {clean_name}, Patient Age: {clean_age} \nPatient ID: P{new_id}", fg="green")
    upload_button.config(text="Upload X-Ray Image", fg="black")

#The search function to find patients by name or ID, which is called when the user clicks the search button
def search_input():
    user_input = search_box.get()
    if not user_input.strip():
        search_result_label.config(text="Error: Search input cannot be blank", fg="red")
        return
    results = search_patient(user_input)
    if results:
        result_text = "Search Results:\n" + "\n".join([f"ID: P{row[0]}, Name: {row[1]}, Age: {row[2]}" for row in results])
        search_result_label.config(text=result_text, fg="green")
    else:
        search_result_label.config(text="No patients found matching the search criteria.", fg="blue")

#The main GUI code for the application
app = tk.Tk()
app.title("Dentikonnect")
app.geometry("375x350")
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
search_box = tk.Entry(app)
search_box.grid(row=5, column=1, padx=20, pady=10, sticky="ew")
search_box.bind('<Return>', lambda event: search_input())
search_label = tk.Label(app, text="Search by Name or ID:")
search_label.grid(row=5, column=0, padx=20, pady=10, sticky="w")
search_result_label = tk.Label(app, text="", wraplength=400)
search_result_label.grid(row=6, column=0, columnspan=2, padx=20, pady=10)
app.mainloop()