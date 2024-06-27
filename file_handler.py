import tkinter as tk
from tkinter import filedialog

def get_file_path(file_type: str) -> str:
    global file_path
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)  # Aktiviere das Tkinter-Top-Level-Fenster

    if file_type == 'input':
        file_path = filedialog.askopenfilename(parent=root, title='Select the input file')
    elif file_type == 'output':
        file_path = filedialog.asksaveasfilename(parent=root, title='Select the output file location')

    root.attributes("-topmost", False)  # Deaktiviere das Tkinter-Top-Level-Fenster
    return file_path

def get_folder_path() -> str:
    root = tk.Tk()
    root.withdraw()  # Versteckt das Tkinter-Hauptfenster
    folder_path = filedialog.askdirectory(parent=root, title='Select the folder')  # Öffnet den Dialog zur Ordnerauswahl
    root.destroy()  # Schließt das Tkinter-Fenster nach der Auswahl
    return folder_path