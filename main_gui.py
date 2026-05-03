import tkinter as tk
app = tk.Tk()
app.title("Dentikonnect")
app.geometry("500x500")
#Entry for the patient's name
name = tk.Entry(app)
name.grid(row=0, column=1, padx=20, pady=10, sticky="ew")
name_label = tk.Label(app, text="What is the Patient's Name?:")
name_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
age = tk.Entry(app)
age.grid(row=1, column=1, padx=20, pady=10, sticky="ew")
age_label = tk.Label(app, text="What is the Patient's Age?:")
age_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
app.mainloop()