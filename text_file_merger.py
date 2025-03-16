#!/usr/bin/env python3
"""
Text File Merger
This program allows users to merge multiple text files into a single output file.
"""

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime

class TextFileMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text File Merger")
        self.root.geometry("700x500")
        self.root.minsize(600, 400)
        
        # Configure the main frame
        main_frame = tk.Frame(root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title label
        title_label = tk.Label(
            main_frame, 
            text="Text File Merger",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Description
        description = tk.Label(
            main_frame,
            text="Select multiple text files to merge them into a single file.\n"
                 "Files will be merged in the order they appear in the list.",
            justify=tk.CENTER
        )
        description.pack(pady=(0, 10))
        
        # Create control frame (for buttons)
        control_frame = tk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=10)
        
        # Buttons for file selection
        self.add_button = tk.Button(
            control_frame,
            text="Add Files",
            command=self.add_files,
            width=15
        )
        self.add_button.grid(row=0, column=0, padx=5)
        
        self.remove_button = tk.Button(
            control_frame,
            text="Remove Selected",
            command=self.remove_selected,
            width=15,
            state=tk.DISABLED
        )
        self.remove_button.grid(row=0, column=1, padx=5)
        
        self.clear_button = tk.Button(
            control_frame,
            text="Clear All",
            command=self.clear_all,
            width=15,
            state=tk.DISABLED
        )
        self.clear_button.grid(row=0, column=2, padx=5)
        
        self.move_up_button = tk.Button(
            control_frame,
            text="Move Up",
            command=self.move_up,
            width=15,
            state=tk.DISABLED
        )
        self.move_up_button.grid(row=0, column=3, padx=5)
        
        self.move_down_button = tk.Button(
            control_frame,
            text="Move Down",
            command=self.move_down,
            width=15,
            state=tk.DISABLED
        )
        self.move_down_button.grid(row=0, column=4, padx=5)
        
        # Options frame
        options_frame = tk.Frame(main_frame)
        options_frame.pack(fill=tk.X, pady=10)
        
        # File separator option
        separator_label = tk.Label(options_frame, text="File Separator:")
        separator_label.grid(row=0, column=0, padx=(0, 5), sticky=tk.W)
        
        self.separator_var = tk.StringVar(value="newline")
        separator_options = ["newline", "double newline", "line of dashes", "custom"]
        self.separator_dropdown = ttk.Combobox(
            options_frame, 
            textvariable=self.separator_var,
            values=separator_options,
            width=15
        )
        self.separator_dropdown.grid(row=0, column=1, padx=5, sticky=tk.W)
        self.separator_dropdown.bind("<<ComboboxSelected>>", self.update_custom_separator)
        
        # Custom separator entry
        self.custom_separator_var = tk.StringVar()
        self.custom_separator_entry = tk.Entry(
            options_frame,
            textvariable=self.custom_separator_var,
            width=20,
            state=tk.DISABLED
        )
        self.custom_separator_entry.grid(row=0, column=2, padx=5, sticky=tk.W)
        
        # Add file headers checkbox
        self.add_headers_var = tk.BooleanVar(value=True)
        self.add_headers_check = tk.Checkbutton(
            options_frame,
            text="Add file headers",
            variable=self.add_headers_var
        )
        self.add_headers_check.grid(row=0, column=3, padx=5, sticky=tk.W)
        
        # Files listbox with scrollbar
        list_frame = tk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Scrollbars
        y_scrollbar = tk.Scrollbar(list_frame)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        x_scrollbar = tk.Scrollbar(list_frame, orient=tk.HORIZONTAL)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Files listbox
        self.files_listbox = tk.Listbox(
            list_frame,
            selectmode=tk.EXTENDED,
            yscrollcommand=y_scrollbar.set,
            xscrollcommand=x_scrollbar.set
        )
        self.files_listbox.pack(fill=tk.BOTH, expand=True)
        y_scrollbar.config(command=self.files_listbox.yview)
        x_scrollbar.config(command=self.files_listbox.xview)
        self.files_listbox.bind("<<ListboxSelect>>", self.on_file_select)
        
        # Status label
        self.status_label = tk.Label(
            main_frame,
            text="Ready. Add text files to begin.",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            padx=5,
            pady=5
        )
        self.status_label.pack(fill=tk.X, pady=(10, 0))
        
        # Merge button
        self.merge_button = tk.Button(
            main_frame,
            text="Merge Files",
            command=self.merge_files,
            height=2,
            bg="#4CAF50",
            fg="white",
            state=tk.DISABLED
        )
        self.merge_button.pack(fill=tk.X, pady=(10, 0))
        
        # Store file paths
        self.file_paths = []
    
    def update_custom_separator(self, event=None):
        if self.separator_var.get() == "custom":
            self.custom_separator_entry.config(state=tk.NORMAL)
        else:
            self.custom_separator_entry.config(state=tk.DISABLED)
    
    def add_files(self):
        filetypes = [("Text Files", "*.txt"), ("All Files", "*.*")]
        files = filedialog.askopenfilenames(
            title="Select Text Files to Merge",
            filetypes=filetypes
        )
        
        if files:
            for file_path in files:
                if file_path not in self.file_paths:
                    self.file_paths.append(file_path)
                    self.files_listbox.insert(tk.END, file_path)
            
            self.update_ui_state()
            self.status_label.config(text=f"Added {len(files)} file(s). Total: {len(self.file_paths)}")
    
    def remove_selected(self):
        selected_indices = self.files_listbox.curselection()
        if not selected_indices:
            return
        
        # Remove in reverse order to maintain correct indices
        for index in sorted(selected_indices, reverse=True):
            self.files_listbox.delete(index)
            self.file_paths.pop(index)
        
        self.update_ui_state()
        self.status_label.config(text=f"Removed {len(selected_indices)} file(s). Remaining: {len(self.file_paths)}")
    
    def clear_all(self):
        self.files_listbox.delete(0, tk.END)
        self.file_paths.clear()
        self.update_ui_state()
        self.status_label.config(text="All files cleared.")
    
    def move_up(self):
        selected_indices = self.files_listbox.curselection()
        if not selected_indices or 0 in selected_indices:
            return
        
        # Only move the first selected item
        index = selected_indices[0]
        
        # Swap items in both the listbox and file_paths
        file_path = self.file_paths[index]
        self.file_paths[index] = self.file_paths[index-1]
        self.file_paths[index-1] = file_path
        
        # Update listbox
        self.files_listbox.delete(index)
        self.files_listbox.insert(index-1, file_path)
        self.files_listbox.select_set(index-1)
        self.files_listbox.see(index-1)
    
    def move_down(self):
        selected_indices = self.files_listbox.curselection()
        if not selected_indices or len(self.file_paths) - 1 in selected_indices:
            return
        
        # Only move the first selected item
        index = selected_indices[0]
        
        # Swap items in both the listbox and file_paths
        file_path = self.file_paths[index]
        self.file_paths[index] = self.file_paths[index+1]
        self.file_paths[index+1] = file_path
        
        # Update listbox
        self.files_listbox.delete(index)
        self.files_listbox.insert(index+1, file_path)
        self.files_listbox.select_set(index+1)
        self.files_listbox.see(index+1)
    
    def on_file_select(self, event=None):
        selected = self.files_listbox.curselection()
        has_selection = len(selected) > 0
        
        # Update button states based on selection
        self.remove_button.config(state=tk.NORMAL if has_selection else tk.DISABLED)
        
        # For move up/down, we need single selection
        if len(selected) == 1:
            index = selected[0]
            self.move_up_button.config(state=tk.NORMAL if index > 0 else tk.DISABLED)
            self.move_down_button.config(state=tk.NORMAL if index < len(self.file_paths) - 1 else tk.DISABLED)
        else:
            self.move_up_button.config(state=tk.DISABLED)
            self.move_down_button.config(state=tk.DISABLED)
    
    def update_ui_state(self):
        has_files = len(self.file_paths) > 0
        
        # Update button states based on file list
        self.clear_button.config(state=tk.NORMAL if has_files else tk.DISABLED)
        self.merge_button.config(state=tk.NORMAL if has_files else tk.DISABLED)
        
        # Also update selection-dependent buttons
        self.on_file_select()
    
    def get_separator(self):
        separator_type = self.separator_var.get()
        
        if separator_type == "newline":
            return "\n"
        elif separator_type == "double newline":
            return "\n\n"
        elif separator_type == "line of dashes":
            return "\n\n" + "-" * 80 + "\n\n"
        elif separator_type == "custom":
            custom_sep = self.custom_separator_var.get()
            return custom_sep if custom_sep else "\n"
        else:
            return "\n"
    
    def merge_files(self):
        if not self.file_paths:
            messagebox.showinfo("No Files", "Please add text files to merge.")
            return
        
        # Ask for output file
        output_path = filedialog.asksaveasfilename(
            title="Save Merged File As",
            defaultextension=".txt",
            filetypes=[("Text File", "*.txt"), ("All Files", "*.*")]
        )
        
        if not output_path:
            self.status_label.config(text="Merge cancelled.")
            return
        
        try:
            with open(output_path, 'w', encoding='utf-8') as outfile:
                separator = self.get_separator()
                add_headers = self.add_headers_var.get()
                
                # Write timestamp at the top
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                outfile.write(f"# Merged file created on {timestamp}\n")
                outfile.write(f"# Contains {len(self.file_paths)} text files\n\n")
                
                for i, file_path in enumerate(self.file_paths):
                    # Add separator between files (except before the first file)
                    if i > 0:
                        outfile.write(separator)
                    
                    # Add file header if enabled
                    if add_headers:
                        file_name = os.path.basename(file_path)
                        outfile.write(f"### FILE {i+1}: {file_name} ###\n")
                    
                    # Read and write file content
                    try:
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            content = infile.read()
                            outfile.write(content)
                    except Exception as e:
                        messagebox.showwarning(
                            "File Error", 
                            f"Error reading file {file_path}:\n{str(e)}\n\nContinuing with other files."
                        )
            
            messagebox.showinfo(
                "Merge Complete", 
                f"Successfully merged {len(self.file_paths)} files into:\n{output_path}"
            )
            self.status_label.config(text=f"Merged {len(self.file_paths)} files to {os.path.basename(output_path)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to merge files:\n{str(e)}")
            self.status_label.config(text="Merge failed. See error message.")

def main():
    root = tk.Tk()
    app = TextFileMergerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()