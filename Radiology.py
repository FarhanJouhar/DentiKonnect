#============================================================================================
#Radiology Tab
#============================================================================================
import tkinter as tk
from patient_manager import search_patient, save_patient_xray
import base64
from tkinter import filedialog

current_patient_id = None
current_xray_path = None

def Radiology_tab(notebook):
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
    
    radiology_tab = tk.Frame(notebook)
    notebook.add(radiology_tab, text="Dental Imaging")
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