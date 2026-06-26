#===============================================================
#Patient Registration Tab
#===============================================================
import tkinter as tk
from tkinter import ttk
from patient_manager import process_patient_data, save_patient_to_db, search_patient, save_visit_to_db

Medical_BG = "#FFFFFF"
Text_Colour = "#2D3748"

patient_id = None

#Function to create the patient registration tab with all the necessary input fields and labels
def registration_tab(notebook):
    def patient_lookup():
        global patient_id
        user_input = lookup_box.get()
        if not user_input.strip():
            lookup_label.config(text="Error: Search input cannot be blank", foreground="red")
            return
        results = search_patient(user_input.lower())
        if results :
            patient_info = results[0]
            patient_id = patient_info[0]
            name_input.config(state="normal")
            name_input.delete(0, tk.END)
            name_input.insert(0, patient_info[1])
            name_input.config(state="readonly")
            age_input.config(state="normal")
            age_input.delete(0, tk.END)
            age_input.insert(0, patient_info[2])
            age_input.config(state="readonly")
            gender_input.config(state="normal")
            gender_var.set(patient_info[3])
            gender_input.config(state="readonly") 
        else:
            lookup_label.config(text="No patient found with that ID or name. Please enter new patient details.", foreground="red")
            result_label.config(text="No patient found. Please register a new patient.", foreground="red")
            name_input.config(state="normal")
            age_input.config(state="normal")
            gender_input.config(state="normal")
            patient_id = None
                             
    #Function to submit the data after going through process_patient_data for validation and then to database using save_patient_to_db
    def submit_data():
            global patient_id
            cc = complaint_input.get("1.0", tk.END).strip() #chief complaint
            hpi = history_input.get("1.0", tk.END).strip() #history of present illness
            pmh = Medical_history_input.get("1.0", tk.END).strip() #past medical history
            pdh = Past_dental_history_input.get("1.0", tk.END).strip() #past dental history
            ph = Personal_history_input.get("1.0", tk.END).strip() #personal history
            pd = prov_diag_input.get().strip() #provisional diagnosis
            if patient_id:
                 save_visit_to_db(patient_id, cc, hpi, pmh, pdh, ph, pd, None, None, None, None)
                 result_label.config(text=f"Success! Visit data saved for Patient ID: P{patient_id}", foreground="green")
            else:
                name = name_input.get().strip()
                age = age_input.get().strip()
                gender = gender_var.get()
                result = process_patient_data(name, age, gender)
                if isinstance(result, str):
                    result_label.config(text=result, foreground="red")
                    return
                clean_name, clean_age, clean_gender = result
                new_id = save_patient_to_db(clean_name, clean_age, clean_gender)
                save_visit_to_db(new_id, cc, hpi, pmh, pdh, ph, pd, None, None, None, None)
                result_label.config(text=f"Success!\nPatient Name: {clean_name}, Patient Age: {clean_age}\n Patient Gender: {clean_gender} \nPatient ID: P{new_id}", foreground="green")
    
    entry_tab = ttk.Frame(notebook)
    notebook.add(entry_tab, text="Patient Registration")
    lookup_label = ttk.Label(entry_tab, text="Existing Patient? Search by ID or Name:")
    lookup_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
    lookup_box = ttk.Entry(entry_tab)
    lookup_box.grid(row=0, column=1, padx=20, pady=10, sticky="ew")
    lookup_box.bind("<Return>", lambda _: patient_lookup())
    lookup_button = ttk.Button(entry_tab, text="Look Up", command=patient_lookup)
    lookup_button.grid(row=0, column=2, padx=5, pady=10)
    name_input = ttk.Entry(entry_tab)
    name_input.grid(row=1, column=1, padx=20, pady=10, sticky="ew")
    name_label = ttk.Label(entry_tab, text="Patient's Name:")
    name_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
    age_input = ttk.Entry(entry_tab)
    age_input.grid(row=2, column=1, padx=20, pady=10, sticky="ew")
    age_label = ttk.Label(entry_tab, text="Patient's Age:")
    age_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")
    gender_var = tk.StringVar(entry_tab)
    gender_var.set("Select Gender")
    gender_input = ttk.OptionMenu(entry_tab, gender_var, "Select Gender", "Male", "Female", "Other")
    gender_input.grid(row=3, column=1, padx=20, pady=10, sticky="ew")
    gender_label = ttk.Label(entry_tab, text="Patient's Gender:")
    gender_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")
    complaint_input = tk.Text(entry_tab , height=4, background=Medical_BG, foreground=Text_Colour)
    complaint_input.grid(row=4, column=1, rowspan=3, columnspan=1, padx=20, pady=10, sticky="ew")
    complaint_label = ttk.Label(entry_tab, text="Chief Complaint:")
    complaint_label.grid(row=4, column=0, padx=20, pady=10, sticky="w")
    history_input = tk.Text(entry_tab , height=4, background=Medical_BG, foreground=Text_Colour)
    history_input.grid(row=7, column=1, rowspan=3, columnspan=1, padx=20, pady=10, sticky="ew")
    history_label = ttk.Label(entry_tab, text="History of Present Illness:")
    history_label.grid(row=7, column=0, padx=20, pady=10, sticky="w")
    Medical_history_input = tk.Text(entry_tab , height=4, background=Medical_BG, foreground=Text_Colour)
    Medical_history_input.grid(row=10, column=1, rowspan=3, columnspan=1, padx=20, pady=10, sticky="ew")
    Medical_history_label = ttk.Label(entry_tab, text="Past Medical History:")
    Medical_history_label.grid(row=10, column=0, padx=20, pady=10, sticky="w")
    Past_dental_history_input = tk.Text(entry_tab , height=4, background=Medical_BG, foreground=Text_Colour)
    Past_dental_history_input.grid(row=13, column=1, rowspan=3, columnspan=1, padx=20, pady=10, sticky="ew")
    Past_dental_history_label = ttk.Label(entry_tab, text="Past Dental History:")
    Past_dental_history_label.grid(row=13, column=0, padx=20, pady=10, sticky="w")
    Personal_history_input = tk.Text(entry_tab , height=4, background=Medical_BG, foreground=Text_Colour)
    Personal_history_input.grid(row=16, column=1, rowspan=3, columnspan=1, padx=20, pady=10, sticky="ew")
    Personal_history_label = ttk.Label(entry_tab, text="Personal History:")
    Personal_history_label.grid(row=16, column=0, padx=20, pady=10, sticky="w")
    prov_diag_input = ttk.Entry(entry_tab)
    prov_diag_input.grid(row=19, column=1, padx=20, pady=10, sticky="ew")
    prov_diag_label = ttk.Label(entry_tab, text="Provisional Diagnosis:")
    prov_diag_label.grid(row=19, column=0, padx=20, pady=10, sticky="w")
    result_label = ttk.Label(entry_tab, text="", wraplength=400, justify="center")
    result_label.grid(row=20, column=0, columnspan=2, padx=20, pady=10)
    submit_button = ttk.Button(entry_tab, text="Submit", command=submit_data)
    submit_button.grid(row=21, column=0, columnspan=2, pady=10)