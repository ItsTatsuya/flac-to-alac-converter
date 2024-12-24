import tkinter as tk
import sv_ttk
from tkinter import filedialog, ttk
from pathlib import Path
import threading
from converter import FlacConverter
import os
from tkinterdnd2 import DND_FILES, TkinterDnD
import logging
import requests
import zipfile
import sys
import shutil

class ConverterGUI:
    def __init__(self):
        self.root = TkinterDnD.Tk()  # Use TkinterDnD instead of regular Tk
        self.root.title("FLAC to ALAC Folder Converter")
        self.root.geometry("800x600")
        self.converter = FlacConverter()
        self.files = []
        
        # Initialize logger
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        self.setup_ui()
        
    def setup_ui(self):
        # File list with drag-drop support
        list_frame = ttk.LabelFrame(self.root, text="FLAC Files (Drag & Drop Here)")
        list_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.file_list = tk.Listbox(list_frame, selectmode=tk.EXTENDED)
        self.file_list.pack(side="left", fill="both", expand=True)
        
        # Enable drag and drop
        self.file_list.drop_target_register(DND_FILES)
        self.file_list.dnd_bind('<<Drop>>', self.handle_drop)
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.file_list.yview)
        scrollbar.pack(side="right", fill="y")
        self.file_list.config(yscrollcommand=scrollbar.set)
        
        # Controls frame
        controls = ttk.Frame(self.root)
        controls.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(controls, text="Add Files", command=self.select_files).pack(side="left", padx=5)
        ttk.Button(controls, text="Add Folder", command=self.select_folder).pack(side="left", padx=5)
        ttk.Button(controls, text="Clear List", command=self.clear_files).pack(side="left", padx=5)
               
        # Output selection
        output_frame = ttk.LabelFrame(self.root, text="Output Folder")
        output_frame.pack(fill="x", padx=5, pady=5)
        
        self.output_path = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.output_path).pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(output_frame, text="Browse", command=self.select_output).pack(side="right", padx=5)
        
        # Status and progress
        self.status_var = tk.StringVar(value="Drop FLAC files here or use Add buttons")
        ttk.Label(self.root, textvariable=self.status_var).pack(pady=5)
        
        self.progress = ttk.Progressbar(self.root, mode='determinate')
        self.progress.pack(fill="x", padx=5, pady=5)
        
        # Convert button
        ttk.Button(self.root, text="Convert Files", command=self.start_conversion).pack(pady=10)

    def handle_drop(self, event):
        """Handle drag and drop events"""
        # Get the raw data from the drop event
        raw_data = event.data
        
        # Handle file paths with spaces correctly
        if raw_data.startswith('{'):
            # Multiple files were dropped
            files = raw_data.strip('{}').split('} {')
        else:
            # Single file was dropped
            files = [raw_data]
        
        # Clean up file paths
        files = [f.strip('"').strip("'") for f in files]
        # Convert to absolute paths
        files = [os.path.abspath(f) for f in files]
        
        # Filter for actual FLAC files
        valid_files = [f for f in files if os.path.isfile(f) and f.lower().endswith('.flac')]
        
        if valid_files:
            self.add_files(valid_files)
        else:
            self.status_var.set("No valid FLAC files were dropped")

    def add_files(self, files):
        """Add files to the conversion list"""
        for file in files:
            try:
                file_path = Path(file).resolve()
                if file_path.suffix.lower() == '.flac' and str(file_path) not in self.files:
                    self.files.append(str(file_path))
                    self.file_list.insert(tk.END, f"{len(self.files)}. {file_path.name}")
                    self.logger.info(f"Added file: {file_path}")
            except Exception as e:
                self.logger.error(f"Error adding file {file}: {str(e)}")
        
        # Update progress bar maximum value
        self.progress['maximum'] = len(self.files)
        self.progress['value'] = 0
        self.update_status()

    def clear_files(self):
        """Clear the file list and reset the progress bar"""
        self.files.clear()
        self.file_list.delete(0, tk.END)
        self.progress['value'] = 0  # Reset progress bar
        self.status_var.set("Waiting for files...")
        self.update_status()

    def update_status(self):
        self.status_var.set(f"Ready to convert {len(self.files)} files")

    def select_files(self):
        files = filedialog.askopenfilenames(filetypes=[("FLAC files", "*.flac")])
        self.add_files(files)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            files = Path(folder).rglob("*.flac")
            self.add_files([str(f) for f in files])

    def select_output(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_path.set(folder)

    def start_conversion(self):
        if not self.files:
            self.status_var.set("No files to convert")
            return
        if not self.output_path.get():
            self.status_var.set("Please select output folder")
            return

        self.progress['maximum'] = len(self.files)
        self.progress['value'] = 0
        
        def convert():
            results = {'success': [], 'failed': []}
            for i, file in enumerate(self.files, 1):
                try:
                    self.converter.convert_file(file, self.output_path.get())
                    results['success'].append(file)
                except Exception as e:
                    print(f"Error converting {file}: {str(e)}")
                    results['failed'].append(file)
                self.progress['value'] = i
                self.status_var.set(f"Converting file {i} of {len(self.files)}")
            
            self.status_var.set(f"Completed: {len(results['success'])} converted, {len(results['failed'])} failed")

        threading.Thread(target=convert, daemon=True).start()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ConverterGUI()
    sv_ttk.set_theme("dark")
    app.run()