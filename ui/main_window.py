import customtkinter as ctk
from tkinter import filedialog
from forge_core.builder import build_executable
import threading

class MainWindow(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)

        # --- Script Selection ---
        self.script_path = ctk.StringVar()
        self.script_frame = ctk.CTkFrame(self)
        self.script_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.script_frame.grid_columnconfigure(1, weight=1)

        self.script_label = ctk.CTkLabel(self.script_frame, text="Python Script/Folder:")
        self.script_label.grid(row=0, column=0, padx=10, pady=10)

        self.script_entry = ctk.CTkEntry(self.script_frame, textvariable=self.script_path)
        self.script_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.browse_button = ctk.CTkButton(self.script_frame, text="Browse", command=self.browse_script)
        self.browse_button.grid(row=0, column=2, padx=10, pady=10)

        # --- Project Name ---
        self.project_name = ctk.StringVar()
        self.name_frame = ctk.CTkFrame(self)
        self.name_frame.grid(row=1, column=0, padx=10, pady=0, sticky="ew")

        self.name_label = ctk.CTkLabel(self.name_frame, text="Project Name:")
        self.name_label.grid(row=0, column=0, padx=10, pady=10)

        self.name_entry = ctk.CTkEntry(self.name_frame, textvariable=self.project_name)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # --- Build Options ---
        self.options_frame = ctk.CTkFrame(self)
        self.options_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        
        self.onefile_var = ctk.BooleanVar(value=True)
        self.onefile_check = ctk.CTkCheckBox(self.options_frame, text="One File", variable=self.onefile_var)
        self.onefile_check.grid(row=0, column=0, padx=10, pady=10)

        self.noconsole_var = ctk.BooleanVar(value=True)
        self.noconsole_check = ctk.CTkCheckBox(self.options_frame, text="No Console", variable=self.noconsole_var)
        self.noconsole_check.grid(row=0, column=1, padx=10, pady=10)

        # --- Icon and Output ---
        self.icon_path = ctk.StringVar()
        self.output_dir = ctk.StringVar()
        self.path_frame = ctk.CTkFrame(self)
        self.path_frame.grid(row=3, column=0, padx=10, pady=0, sticky="ew")
        self.path_frame.grid_columnconfigure(1, weight=1)

        self.icon_label = ctk.CTkLabel(self.path_frame, text="Icon:")
        self.icon_label.grid(row=0, column=0, padx=10, pady=10)
        self.icon_entry = ctk.CTkEntry(self.path_frame, textvariable=self.icon_path)
        self.icon_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.icon_button = ctk.CTkButton(self.path_frame, text="Browse", command=self.browse_icon)
        self.icon_button.grid(row=0, column=2, padx=10, pady=10)

        self.output_label = ctk.CTkLabel(self.path_frame, text="Output Dir:")
        self.output_label.grid(row=1, column=0, padx=10, pady=10)
        self.output_entry = ctk.CTkEntry(self.path_frame, textvariable=self.output_dir)
        self.output_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.output_button = ctk.CTkButton(self.path_frame, text="Browse", command=self.browse_output_dir)
        self.output_button.grid(row=1, column=2, padx=10, pady=10)

        # --- Build Button ---
        self.build_button = ctk.CTkButton(self, text="Build EXE", command=self.build_exe)
        self.build_button.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        # --- Log View ---
        self.log_view = ctk.CTkTextbox(self, height=200)
        self.log_view.grid(row=5, column=0, padx=10, pady=10, sticky="nsew")
        self.grid_rowconfigure(5, weight=1)

        
    def browse_script(self):
        # Allow user to select a file or a directory
        path = filedialog.askopenfilename(title="Select a Python Script", filetypes=[("Python Files", "*.py"), ("All files", "*.*")])
        if not path:
            path = filedialog.askdirectory(title="Select Project Folder")
        if path:
            self.script_path.set(path)

    def browse_icon(self):
        path = filedialog.askopenfilename(title="Select an Icon", filetypes=[("Icon Files", "*.ico"), ("All files", "*.*")])
        if path:
            self.icon_path.set(path)

    def browse_output_dir(self):
        path = filedialog.askdirectory(title="Select Output Directory")
        if path:
            self.output_dir.set(path)

    def log_message(self, message):
        self.log_view.insert("end", message)
        self.log_view.see("end")

    def build_exe(self):
        self.log_view.delete("1.0", "end")
        self.log_message("Starting build...\n")
        
        options = {
            "script": self.script_path.get(),
            "name": self.project_name.get(),
            "onefile": self.onefile_var.get(),
            "noconsole": self.noconsole_var.get(),
            "icon": self.icon_path.get(),
            "output_dir": self.output_dir.get()
        }
        
        build_thread = threading.Thread(target=build_executable, args=(options, self.log_message))
        build_thread.start()
