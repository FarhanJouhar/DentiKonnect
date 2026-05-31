#============================================================================================
#Diagnosis Tab
#============================================================================================
import tkinter as tk

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
    tk.Label(data_frame, text="Enter Patient ID:").grid(row=1, column=0, sticky="w", padx=10, pady=10)
    diag_search_input = tk.Entry(data_frame, width=15)
    diag_search_input.grid(row=1, column=1, sticky="w", padx=5, pady=10)
    tk.Label(data_frame, text="Enter Patient Name:").grid(row=2, column=0, sticky="w", padx=10, pady=10)
    diag_search_name = tk.Entry(data_frame, width=15)
    diag_search_name.grid(row=2, column=1, sticky="w", padx=5, pady=10)