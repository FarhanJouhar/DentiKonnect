#============================================================================================
#Diagnosis Tab
#============================================================================================
import tkinter as tk
from patient_manager import search_patient
import base64

doctor_login = False

def diagnosis_tab(notebook):
    #The function to unlock the patient data after verifying the password
    def unlock_patient_data():
        global doctor_login
        SECRET_DOC_PASSWORD = "THDentikonnect2026"  #This is not the safest way to handle passwords, but for the sake of this project we will use this method. In a production environment, consider using environment variables or a secure vault.
        if password_input.get() == SECRET_DOC_PASSWORD:
            auth_status_label.config(text="Valid Password! Access Granted.", fg="green")
            doctor_login = True
            auth_frame.pack_forget()
            data_frame.pack(pady=10)
            return
        else:
            auth_status_label.config(text="Invalid Password! Access Denied.", fg="red")

    def populate_fields(patient_row):
        if patient_row:
            name_field.config(state="normal")
            name_field.delete(0, tk.END)
            name_field.insert(0, patient_row[1])
            name_field.config(state="readonly")
            age_field.config(state="normal")
            age_field.delete(0, tk.END)
            age_field.insert(0, patient_row[2])
            age_field.config(state="readonly")
            gender_field.config(state="normal")
            gender_field.delete(0, tk.END)
            gender_field.insert(0, patient_row[3])
            gender_field.config(state="readonly")
            

    def diagnosis_search():
        global current_patient_id
        user_input = search_box.get()
        if not user_input.strip():
            search_result_label.config(text="Error: Search input cannot be blank", fg="red")
            return
        results = search_patient(user_input)
        if results:
            current_patient_id = results[0][0]
            populate_fields(results[0])
            result_text = f"Search Results: Patient ID: P{current_patient_id} Successfully Loaded"
            search_result_label.config(text=result_text, fg="green")
            if results[0][9]:
                try:
                    # Convert raw bytes to Base64 so Tkinter can read it
                    b64_data = base64.b64encode(results[0][9])
                    photo = tk.PhotoImage(data=b64_data)
                    width_factor = photo.width() // 300
                    height_factor = photo.height() // 300
                    scale_factor = max(1, width_factor, height_factor)
                    shrunk_photo = photo.subsample(scale_factor, scale_factor) # The image will now be resized to fit within a 300x300 box while maintaining aspect ratio
                    display_xray.config(image=shrunk_photo, text="") 
                    display_xray.image = shrunk_photo
                except Exception:
                    search_result_label.config(text="Error: Could not render image.", fg="red")
            else:
                display_xray.config(image="", text="No X-ray on file.")
        else:
            search_result_label.config(text="No patients found matching the search criteria.", fg="blue")
            current_patient_id = None


    diagnosis_tab = tk.Frame(notebook)
    notebook.add(diagnosis_tab, text="Diagnosis")
    auth_frame = tk.Frame(diagnosis_tab)
    auth_frame.pack(pady=40)
    data_frame = tk.Frame(diagnosis_tab)
    tk.Label(auth_frame, text="Medical Staff Authentication Required", fg="red").pack(pady=10)
    password_input = tk.Entry(auth_frame, show="*", width=20)
    password_input.pack(pady=5)
    auth_status_label = tk.Label(auth_frame, text="")
    auth_status_label.pack(pady=5)
    unlock_button = tk.Button(auth_frame, text="Unlock Records", command=unlock_patient_data)
    unlock_button.pack(pady=10)
    search_box = tk.Entry(data_frame)
    search_box.grid(row=0, column=1, padx=20, pady=10, sticky="ew")
    search_box.bind('<Return>', lambda _: diagnosis_search())
    search_label = tk.Label(data_frame, text="Search by Name or ID:")
    search_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
    search_label = tk.Label(data_frame, text="Search by Name or ID:")
    search_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
    search_result_label = tk.Label(data_frame, text="", wraplength=400)
    search_result_label.grid(row=1, column=0, columnspan=2, padx=20, pady=10)
    name_field = tk.Entry(data_frame, state="readonly", width=30)
    name_field.grid(row=2, column=1, padx=20, pady=10, sticky="w")
    name_label = tk.Label(data_frame, text="Patient Name:")
    name_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")
    age_field = tk.Entry(data_frame, state="readonly", width=30)
    age_field.grid(row=3, column=1, padx=20, pady=10, sticky="w")
    age_label = tk.Label(data_frame, text="Patient Age:")
    age_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")
    gender_field = tk.Entry(data_frame, state="readonly", width=30)
    gender_field.grid(row=4, column=1, padx=20, pady=10, sticky="w")
    gender_label = tk.Label(data_frame, text="Patient Gender:")
    gender_label.grid(row=4, column=0, padx=20, pady=10, sticky="w")
    display_xray = tk.Label(data_frame, text="[ X-Ray View ]", bg="black", fg="white")
    display_xray.grid(row=21, column=0, columnspan=2, padx=20, pady=10)