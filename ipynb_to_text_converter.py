#!/usr/bin/env python3
"""
Jupyter Notebook to Text Converter
This script extracts code cells from Jupyter notebooks and saves them as plain text files.
"""

import json
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox

def extract_code_from_notebook(notebook_path):
    """Extract only code cells from a Jupyter notebook."""
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        code_content = []
        
        # Verify this is a Jupyter notebook
        if 'cells' not in notebook:
            raise ValueError("This file does not appear to be a valid Jupyter notebook.")
            
        for cell in notebook['cells']:
            if cell['cell_type'] == 'code':
                # Only extract the source code, not the outputs
                code = ''.join(cell['source'])
                # Add a newline if it doesn't end with one
                if code and not code.endswith('\n'):
                    code += '\n'
                code_content.append(code)
                
        return '\n'.join(code_content)
    except Exception as e:
        raise Exception(f"Error processing {notebook_path}: {str(e)}")

def save_as_text(code_content, output_path):
    """Save the extracted code to a text file."""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(code_content)
        return True
    except Exception as e:
        raise Exception(f"Error saving to {output_path}: {str(e)}")

class NotebookConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Jupyter Notebook to Text Converter")
        self.root.geometry("600x400")
        self.root.minsize(500, 300)
        
        # Configure the main frame
        main_frame = tk.Frame(root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title label
        title_label = tk.Label(
            main_frame, 
            text="Convert Jupyter Notebooks to Text Files",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Description
        description = tk.Label(
            main_frame,
            text="This tool extracts only the code cells from Jupyter notebooks\n"
                 "and saves them as plain text files, excluding all outputs.",
            justify=tk.CENTER
        )
        description.pack(pady=(0, 20))
        
        # Buttons frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        # Select files button
        self.select_button = tk.Button(
            button_frame,
            text="Select Notebook Files",
            command=self.select_files,
            width=20,
            height=2
        )
        self.select_button.grid(row=0, column=0, padx=10)
        
        # Convert button
        self.convert_button = tk.Button(
            button_frame,
            text="Convert Selected Files",
            command=self.convert_files,
            width=20,
            height=2,
            state=tk.DISABLED
        )
        self.convert_button.grid(row=0, column=1, padx=10)
        
        # Status frame
        status_frame = tk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Status label
        self.status_label = tk.Label(
            status_frame,
            text="Ready. Select Jupyter notebook files to begin.",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            padx=5,
            pady=5
        )
        self.status_label.pack(fill=tk.X)
        
        # Selected files list frame
        list_frame = tk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Files listbox
        self.files_listbox = tk.Listbox(
            list_frame,
            selectmode=tk.EXTENDED,
            yscrollcommand=scrollbar.set
        )
        self.files_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.files_listbox.yview)
        
        # Instance variables
        self.selected_files = []
    
    def select_files(self):
        """Open file dialog to select Jupyter notebook files."""
        filetypes = [("Jupyter Notebooks", "*.ipynb"), ("All Files", "*.*")]
        files = filedialog.askopenfilenames(
            title="Select Jupyter Notebook Files",
            filetypes=filetypes
        )
        
        if files:
            self.selected_files = list(files)
            self.files_listbox.delete(0, tk.END)
            for file in self.selected_files:
                self.files_listbox.insert(tk.END, os.path.basename(file))
            
            self.status_label.config(text=f"Selected {len(self.selected_files)} file(s). Ready to convert.")
            self.convert_button.config(state=tk.NORMAL)
        else:
            self.status_label.config(text="No files selected.")
    
    def convert_files(self):
        """Convert selected notebook files to text files."""
        if not self.selected_files:
            messagebox.showinfo("No Files", "Please select notebook files first.")
            return
        
        # Ask for output directory
        output_dir = filedialog.askdirectory(title="Select Output Directory")
        if not output_dir:
            self.status_label.config(text="Conversion cancelled. No output directory selected.")
            return
        
        success_count = 0
        error_messages = []
        
        for notebook_path in self.selected_files:
            try:
                # Extract base filename without extension
                base_name = os.path.splitext(os.path.basename(notebook_path))[0]
                output_path = os.path.join(output_dir, f"{base_name}.txt")
                
                # Extract code and save as text
                code_content = extract_code_from_notebook(notebook_path)
                save_as_text(code_content, output_path)
                
                success_count += 1
            except Exception as e:
                error_messages.append(f"Error converting {os.path.basename(notebook_path)}: {str(e)}")
        
        # Show results
        if error_messages:
            error_text = "\n".join(error_messages)
            messagebox.showerror("Conversion Errors", f"Encountered {len(error_messages)} error(s):\n\n{error_text}")
        
        if success_count > 0:
            messagebox.showinfo("Conversion Complete", 
                              f"Successfully converted {success_count} of {len(self.selected_files)} notebooks to text files.")
            self.status_label.config(text=f"Converted {success_count} of {len(self.selected_files)} notebooks.")
        else:
            self.status_label.config(text="Conversion failed. Please check error messages.")

def main():
    root = tk.Tk()
    app = NotebookConverterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()