#===============================================================
#Patient Registration Tab
#===============================================================
import tkinter as tk
from patient_manager import process_patient_data, save_patient_to_db

#Function to create the patient registration tab with all the necessary input fields and labels
def registration_tab(notebook):
    #Function to submit the data after going through process_patient_data for validation and then to database using save_patient_to_db
    def submit_data():
        name = name_input.get()
        age = age_input.get()
        result = process_patient_data(name, age)
        if isinstance(result, str):
            result_label.config(text=result, fg="red")
        else:
            clean_name, clean_age = result
            gender = gender_var.get()
            cc = complaint_input.get("1.0", tk.END).strip() #chief complaint
            hpi = history_input.get("1.0", tk.END).strip() #history of present illness
            pmh = Medical_history_input.get("1.0", tk.END).strip() #past medical history
            ph = Personal_history_input.get("1.0", tk.END).strip() #personal history
            pd = prov_diag_input.get().strip() #provisional diagnosis
            new_id = save_patient_to_db(clean_name, clean_age, gender, cc, hpi, pmh, ph, pd, None)
            result_label.config(text=f"Success!\nPatient Name: {clean_name}, Patient Age: {clean_age}\n Patient Gender: {gender} \nPatient ID: P{new_id}", fg="green")
    
    entry_tab = tk.Frame(notebook)
    notebook.add(entry_tab, text="Patient Registration")
    name_input = tk.Entry(entry_tab)
    name_input.grid(row=0, column=1, padx=20, pady=10, sticky="ew")
    name_label = tk.Label(entry_tab, text="Patient's Name:")
    name_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
    age_input = tk.Entry(entry_tab)
    age_input.grid(row=1, column=1, padx=20, pady=10, sticky="ew")
    age_label = tk.Label(entry_tab, text="Patient's Age:")
    age_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
    gender_var = tk.StringVar(entry_tab)
    gender_var.set("Select Gender")
    gender_input = tk.OptionMenu(entry_tab, gender_var, "Male", "Female", "Other")
    gender_input.grid(row=2, column=1, padx=20, pady=10, sticky="ew")
    gender_label = tk.Label(entry_tab, text="Patient's Gender:")
    gender_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")
    complaint_input = tk.Text(entry_tab , height=4)
    complaint_input.grid(row=3, column=1, rowspan=3, columnspan=1, padx=20, pady=10, sticky="ew")
    complaint_label = tk.Label(entry_tab, text="Chief Complaint:")
    complaint_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")
    history_input = tk.Text(entry_tab , height=4)
    history_input.grid(row=6, column=1, rowspan=3, columnspan=1, padx=20, pady=10, sticky="ew")
    history_label = tk.Label(entry_tab, text="History of Present Illness:")
    history_label.grid(row=6, column=0, padx=20, pady=10, sticky="w")
    Medical_history_input = tk.Text(entry_tab , height=4)
    Medical_history_input.grid(row=9, column=1, rowspan=3, columnspan=1, padx=20, pady=10, sticky="ew")
    Medical_history_label = tk.Label(entry_tab, text="Past Medical History:")
    Medical_history_label.grid(row=9, column=0, padx=20, pady=10, sticky="w")
    Personal_history_input = tk.Text(entry_tab , height=4)
    Personal_history_input.grid(row=12, column=1, rowspan=3, columnspan=1, padx=20, pady=10, sticky="ew")
    Personal_history_label = tk.Label(entry_tab, text="Personal History:")
    Personal_history_label.grid(row=12, column=0, padx=20, pady=10, sticky="w")
    prov_diag_input = tk.Entry(entry_tab)
    prov_diag_input.grid(row=15, column=1, padx=20, pady=10, sticky="ew")
    prov_diag_label = tk.Label(entry_tab, text="Provisional Diagnosis:")
    prov_diag_label.grid(row=15, column=0, padx=20, pady=10, sticky="w")
    result_label = tk.Label(entry_tab, text="", wraplength=400)
    result_label.grid(row=16, column=0, columnspan=2, padx=20, pady=10)
    submit_button = tk.Button(entry_tab, text="Submit", command=submit_data)
    submit_button.grid(row=18, column=0, columnspan=2, pady=10)