import tkinter as tk
from tkinter import font, ttk
from patient_manager import create_db
from Diagnosis import diagnosis_tab
from Patient_Registration import registration_tab
from Radiology import Radiology_tab
import ctypes

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

#Function to create the database if it doesn't exist, which is called at the start of the application
create_db()

#The main GUI code for the application
app = tk.Tk()
notebook = ttk.Notebook(app)
notebook.grid(row=0, column=0, padx=10, pady=10)
current_dpi = app.winfo_fpixels('1i')
scaling_factor = current_dpi / 77.0
app.tk.call('tk', 'scaling', scaling_factor)
default_font = font.nametofont("TkDefaultFont")
default_font.configure(size=int(9 * scaling_factor))
app.title("Dentikonnect")
app.geometry("880x920")

registration_tab(notebook)
Radiology_tab(notebook)
diagnosis_tab(notebook)

app.mainloop()