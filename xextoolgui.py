import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import sys

class XexToolGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("XexTool GUI Wrapper")
        
        # Directory selection for scanning XEX files
        self.scan_label = tk.Label(root, text="Select Directory to Scan for XEX Files:")
        self.scan_label.pack()
        self.scan_entry = tk.Entry(root, width=50)
        self.scan_entry.pack()
        self.scan_button = tk.Button(root, text="Browse", command=self.browse_directory)
        self.scan_button.pack()
        
        # Options selection
        self.options_frame = tk.Frame(root)
        self.options_frame.pack()
        
        self.option_list = {
            "-l": "Print extended info",
            "-b": "Dump basefile",
            "-i": "Dump to IDC file",
            "-r a": "Remove all limits",
            "-m d": "Convert to devkit",
            "-m r": "Convert to retail",
            "-e u": "Unencrypt XEX",
            "-e e": "Encrypt XEX",
            "-c u": "Uncompress XEX",
            "-c c": "Compress XEX",
            "-o": "Output XEX file"
        }
        
        self.option_vars = {}
        for opt, desc in self.option_list.items():
            var = tk.BooleanVar()
            chk = tk.Checkbutton(self.options_frame, text=desc, variable=var)
            chk.pack(anchor="w")
            self.option_vars[opt] = var
        
        # Output file selection
        self.output_file_label = tk.Label(root, text="Output XEX File (optional):")
        self.output_file_label.pack()
        self.output_file_entry = tk.Entry(root, width=50)
        self.output_file_entry.pack()
        self.output_file_button = tk.Button(root, text="Browse", command=self.browse_output)
        self.output_file_button.pack()
        
        # Scan and Patch button
        self.scan_patch_button = tk.Button(root, text="Scan and Patch XEX Files", command=self.scan_and_patch)
        self.scan_patch_button.pack()
    
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.scan_entry.delete(0, tk.END)
            self.scan_entry.insert(0, directory)
    
    def browse_output(self):
        filename = filedialog.asksaveasfilename(defaultextension=".xex", filetypes=[("XEX Files", "*.xex")])
        if filename:
            self.output_file_entry.delete(0, tk.END)
            self.output_file_entry.insert(0, filename)
    
    def scan_and_patch(self):
        directory = self.scan_entry.get().strip()
        if not directory or not os.path.isdir(directory):
            messagebox.showerror("Error", "Please select a valid directory.")
            return
        
        xex_files = []
        for root_dir, _, files in os.walk(directory):
            xex_files.extend([os.path.join(root_dir, f) for f in files if f.endswith(".xex")])
        
        if not xex_files:
            messagebox.showinfo("No Files Found", "No .xex files found in the selected directory and subdirectories.")
            return
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        xextool_path = os.path.join(script_dir, "xextool.exe")
        
        if sys.platform == "darwin":
            base_cmd = ["/Applications/CrossOver.app/Contents/SharedSupport/CrossOver/bin/wine", xextool_path]
        elif sys.platform == "linux":
            base_cmd = ["wine", xextool_path]
        else:
            base_cmd = [xextool_path]
        
        options = [opt for opt, var in self.option_vars.items() if var.get()]
        
        for xex_file in xex_files:
            cmd = base_cmd + options + [xex_file]
            
            if "-o" in options:
                output_file = self.output_file_entry.get().strip()
                if output_file:
                    cmd.extend(["-o", output_file])
            
            try:
                process = subprocess.run(cmd, check=True, text=True, capture_output=True)
                output = process.stdout.strip()
                error_output = process.stderr.strip()
                
                if output:
                    print(f"XexTool Output for {xex_file}:\n", output)
                if error_output:
                    print(f"XexTool Errors for {xex_file}:\n", error_output)
                
            except subprocess.CalledProcessError as e:
                print(f"XexTool Execution Failed for {xex_file}:\n", e.stderr)
        
        messagebox.showinfo("Success", "Patching completed for all detected XEX files.")

if __name__ == "__main__":
    root = tk.Tk()
    app = XexToolGUI(root)
    root.mainloop()
