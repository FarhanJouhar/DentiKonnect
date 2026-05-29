import tkinter as tk
from tkinter import filedialog, font, ttk
import base64
from patient_manager import process_patient_data, save_patient_to_db, create_db, search_patient, save_patient_xray
import ctypes

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

#Function to create the database if it doesn't exist, which is called at the start of the application
create_db()
current_patient_id = None
current_xray_path = None

#Function to upload the xray image
def upload_image():
    global current_patient_id, current_xray_path
    if not current_patient_id:
        search_result_label.config(text="Error: Please search for a patient before uploading an X-ray.", fg="red")
        return
    path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
    #When a file is selected, it is displayed in the X-ray preview box. It can be verified before clicking "Save X-Ray" to encrypt and save to the patient's profile.
    if path:
        current_xray_path = path
        upload_button.config(text="Image Selected", fg="blue")
        try:
            photo = tk.PhotoImage(file=current_xray_path)
            width_factor = photo.width() // 300
            height_factor = photo.height() // 300
            scale_factor = max(1, width_factor, height_factor)
            shrunk_photo = photo.subsample(scale_factor, scale_factor) # The image will now be resized to fit within a 300x300 box while maintaining aspect ratio
            display_xray.config(image=shrunk_photo, text="") 
            display_xray.image = shrunk_photo
            search_result_label.config(text="Preview loaded. Verify the image and click 'Save X-Ray'.", fg="black")
        except Exception:
            search_result_label.config(text="Error: Could not render image.", fg="red")

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
    upload_button.config(text="Upload X-Ray Image", fg="black")

#The search function to find patients by name or ID, which is called when the user clicks the Enter button
def search_input():
    global current_patient_id
    user_input = search_box.get()
    if not user_input.strip():
        search_result_label.config(text="Error: Search input cannot be blank", fg="red")
        return
    results = search_patient(user_input)
    if results:
        current_patient_id = results[0][0]
        result_text = "Search Results:\n" + "\n".join([f"ID: P{row[0]}, Name: {row[1]}, Age: {row[2]}, Gender: {row[3]}" for row in results])
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

#The function to save the x-ray to the patient's profile after encryption, which is called when the user clicks the "Save X-Ray" button
def save_xray_to_profile():
    global current_patient_id, current_xray_path
    if not current_patient_id:
        search_result_label.config(text="Error: Please search for a patient first.", fg="red")
        return
    if not current_xray_path:
        search_result_label.config(text="Error: No image preview loaded. Click 'Upload' first.", fg="red")
        return
    success = save_patient_xray(current_patient_id, current_xray_path)
    if success is True:
        search_result_label.config(text="Success: X-Ray securely encrypted and saved to profile!", fg="green")
        current_xray_path = None  
        upload_button.config(text="Upload X-Ray Image", fg="black")
    else:
        search_result_label.config(text=f"Database Error: {success}", fg="red")

#The main GUI code for the application
app = tk.Tk()
notebook = ttk.Notebook(app)
notebook.grid(row=0, column=0, padx=10, pady=10)
entry_tab = tk.Frame(notebook)
radiology_tab = tk.Frame(notebook)
notebook.add(entry_tab, text="Patient Registration")
notebook.add(radiology_tab, text="Dental Imaging")
current_dpi = app.winfo_fpixels('1i')
scaling_factor = current_dpi / 77.0
app.tk.call('tk', 'scaling', scaling_factor)
default_font = font.nametofont("TkDefaultFont")
default_font.configure(size=int(9 * scaling_factor))
app.title("Dentikonnect")
app.geometry("880x920")
#===============================================================
#Patient Registration Tab
#===============================================================
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
#============================================================================================
#Radiology Tab
#============================================================================================
search_box = tk.Entry(radiology_tab)
search_box.grid(row=0, column=1, padx=20, pady=10, sticky="ew")
search_box.bind('<Return>', lambda _: search_input())
search_label = tk.Label(radiology_tab, text="Search by Name or ID:")
search_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
search_result_label = tk.Label(radiology_tab, text="", wraplength=400)
search_result_label.grid(row=1, column=0, columnspan=2, padx=20, pady=10)
upload_button = tk.Button(radiology_tab, text="Upload X-Ray Image", command=upload_image)
upload_button.grid(row=2, column=0, columnspan=2, pady=10)
save_xray_button = tk.Button(radiology_tab, text="Save X-Ray", command=save_xray_to_profile)
save_xray_button.grid(row=3, column=0, columnspan=2, pady=10)
display_xray = tk.Label(radiology_tab, text="[ X-Ray View ]", bg="black", fg="white")
display_xray.grid(row=21, column=0, columnspan=2, padx=20, pady=10)
app.mainloop()