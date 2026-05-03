import customtkinter
app = customtkinter.CTk()
app.title("Dentikonnect")
app.geometry("500x500")
#Entry for the patient's name
name = customtkinter.CTkEntry(app, placeholder_text="Name")
name.grid(row=0, column=1, padx=20, pady=10, sticky="ew")
name_label = customtkinter.CTkLabel(app, text="What is the Patient's Name?:")
name_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
age = customtkinter.CTkEntry(app, placeholder_text="Age")
age.grid(row=1, column=1, padx=20, pady=10, sticky="ew")
age_label = customtkinter.CTkLabel(app, text="What is the Patient's Age?:")
age_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
app.mainloop()