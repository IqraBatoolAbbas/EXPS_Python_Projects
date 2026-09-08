import os
import shutil
import ctypes
import tkinter as tk
from tkinter import filedialog, messagebox

# Windows High-DPI Fix (Sharp Text)
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass


class ModernFileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Automated JPG File Organizer")
        self.root.geometry("620x400")
        self.root.resizable(False, False)
        self.root.configure(bg="#ffffff")

        self.selected_files = []  # Selected files list

        # Title Header
        title_label = tk.Label(
            root,
            text="📁 JPG File Organizer",
            font=("Segoe UI", 18, "bold"),
            bg="#ffffff",
            fg="#1a1a1a"
        )
        title_label.pack(pady=(20, 15))

        # 1. Select JPG Files Row (Files will be visible here!)
        self.files_var = tk.StringVar()
        self.create_picker_row(
            "Select JPG Images (Files will be visible):",
            self.files_var,
            self.browse_files,
            btn_text="Browse Files"
        )

        # 2. Destination Folder Row
        self.dest_folder = tk.StringVar()
        self.create_picker_row(
            "Destination Folder (Where to move JPGs):",
            self.dest_folder,
            self.browse_destination,
            btn_text="Select Folder"
        )

        # Process Button
        organize_btn = tk.Button(
            root,
            text="🚀 Move JPG Files",
            font=("Segoe UI", 11, "bold"),
            bg="#107c41",
            fg="white",
            activebackground="#0e6b37",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=15,
            pady=8,
            command=self.move_jpg_files,
            cursor="hand2"
        )
        organize_btn.pack(pady=25)

        # Status Label
        self.status_label = tk.Label(
            root,
            text="Status: Ready",
            font=("Segoe UI", 9, "italic"),
            bg="#ffffff",
            fg="#666666"
        )
        self.status_label.pack(side="bottom", pady=12)

    def create_picker_row(self, label_text, text_var, browse_command, btn_text):
        """Creates an input row with browse button."""
        frame = tk.Frame(self.root, bg="#ffffff")
        frame.pack(fill="x", padx=30, pady=10)

        lbl = tk.Label(
            frame, 
            text=label_text, 
            font=("Segoe UI", 10, "bold"), 
            bg="#ffffff", 
            fg="#333333"
        )
        lbl.pack(anchor="w", pady=(0, 4))

        entry_frame = tk.Frame(frame, bg="#ffffff")
        entry_frame.pack(fill="x", expand=True)

        entry = tk.Entry(
            entry_frame, 
            textvariable=text_var, 
            font=("Segoe UI", 10), 
            bg="#f3f3f3", 
            fg="#1a1a1a",
            relief="flat",
            bd=1,
            state="readonly"
        )
        entry.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 8))

        btn = tk.Button(
            entry_frame,
            text=btn_text,
            font=("Segoe UI", 9, "bold"),
            bg="#0078d4",
            fg="white",
            activebackground="#005a9e",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=12,
            pady=4,
            command=browse_command,
            cursor="hand2"
        )
        btn.pack(side="right")

    def browse_files(self):
        """Allows user to view and select .jpg files directly."""
        files = filedialog.askopenfilenames(
            title="Select JPG Images",
            filetypes=[("JPG Images", "*.jpg *.jpeg"), ("All Files", "*.*")]
        )
        if files:
            self.selected_files = list(files)
            self.files_var.set(f"{len(self.selected_files)} JPG file(s) selected")

    def browse_destination(self):
        """Select destination folder."""
        selected_dir = filedialog.askdirectory(title="Select Destination Folder")
        if selected_dir:
            self.dest_folder.set(selected_dir)

    def move_jpg_files(self):
        dest = self.dest_folder.get().strip()

        if not self.selected_files:
            messagebox.showwarning("No Files Selected", "Please select JPG files first.")
            return

        if not dest:
            messagebox.showwarning("Missing Folder", "Please select a Destination folder.")
            return

        try:
            moved_count = 0
            for file_path in self.selected_files:
                file_name = os.path.basename(file_path)
                dest_path = os.path.join(dest, file_name)

                # Move file
                shutil.move(file_path, dest_path)
                moved_count += 1

            self.status_label.config(text=f"Status: Successfully moved {moved_count} file(s).")
            messagebox.showinfo("Success", f"Done! Moved {moved_count} JPG file(s) successfully.")

            # Reset selection
            self.selected_files = []
            self.files_var.set("")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while moving files:\n{str(e)}")
            self.status_label.config(text="Status: Process failed.")


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernFileOrganizerApp(root)
    root.mainloop()