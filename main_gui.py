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

create_db()

#The main GUI code for the application
app = tk.Tk()
app.title("Dentikonnect")
app.minsize(600, 700)

#We will try to facelift the GUI a little so it doesn't look like a 90's application. This colour scheme may change in the future
style = ttk.Style()
style.theme_use('clam')
Medical_BG = "#F4F6F9"
Text_Colour = "#2D3748"
Dental_Teal = "#0D9488"
style.configure('.', background=Medical_BG, foreground=Text_Colour, font=('Segoe UI', 11))
app.configure(bg=Dental_Teal)
style.configure("TNotebook", background=Dental_Teal, bordercolor=Dental_Teal)

notebook = ttk.Notebook(app)
notebook.grid(row=0, column=0, padx=10, pady=10)
current_dpi = app.winfo_fpixels('1i')
scaling_factor = current_dpi / 77.0
app.tk.call('tk', 'scaling', scaling_factor)
default_font = font.nametofont("TkDefaultFont")
default_font.configure(size=int(11 * scaling_factor))

registration_tab(notebook)
Radiology_tab(notebook)
diagnosis_tab(notebook)

app.mainloop()