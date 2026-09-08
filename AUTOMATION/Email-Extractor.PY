import os
import re
import ctypes
import tkinter as tk
from tkinter import filedialog, messagebox

# ---------------------------------------------------------
# WINDOWS HIGH-DPI SCALING FIX (SHARP TEXT RENDERING)
# ---------------------------------------------------------
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass


class EmailExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Automated Email Address Extractor")
        self.root.geometry("620x400")
        self.root.resizable(False, False)
        self.root.configure(bg="#ffffff")

        self.input_file_path = ""

        # Title Header
        title_label = tk.Label(
            root,
            text="📧 Email Address Extractor",
            font=("Segoe UI", 18, "bold"),
            bg="#ffffff",
            fg="#1a1a1a"
        )
        title_label.pack(pady=(20, 15))

        # 1. Select Text File Row
        self.file_var = tk.StringVar()
        self.create_picker_row(
            "Select Text File (.txt):",
            self.file_var,
            self.browse_text_file,
            btn_text="Browse File"
        )

        # 2. Output File Name Option Row
        self.output_file_var = tk.StringVar(value="extracted_emails.txt")
        self.create_input_row(
            "Save Extracted Emails As:",
            self.output_file_var
        )

        # Process Button
        extract_btn = tk.Button(
            root,
            text="⚡ Extract & Save Emails",
            font=("Segoe UI", 11, "bold"),
            bg="#0078d4",
            fg="white",
            activebackground="#005a9e",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=15,
            pady=8,
            command=self.extract_emails,
            cursor="hand2"
        )
        extract_btn.pack(pady=25)

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
        """Creates a row for selecting file."""
        frame = tk.Frame(self.root, bg="#ffffff")
        frame.pack(fill="x", padx=30, pady=8)

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
            bg="#107c41",
            fg="white",
            activebackground="#0e6b37",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=12,
            pady=4,
            command=browse_command,
            cursor="hand2"
        )
        btn.pack(side="right")

    def create_input_row(self, label_text, text_var):
        """Creates an editable text entry row."""
        frame = tk.Frame(self.root, bg="#ffffff")
        frame.pack(fill="x", padx=30, pady=8)

        lbl = tk.Label(
            frame,
            text=label_text,
            font=("Segoe UI", 10, "bold"),
            bg="#ffffff",
            fg="#333333"
        )
        lbl.pack(anchor="w", pady=(0, 4))

        entry = tk.Entry(
            frame,
            textvariable=text_var,
            font=("Segoe UI", 10),
            bg="#f3f3f3",
            fg="#1a1a1a",
            relief="flat",
            bd=1
        )
        entry.pack(fill="x", ipady=6)

    def browse_text_file(self):
        """Allows user to view and pick .txt file."""
        selected_file = filedialog.askopenfilename(
            title="Select Text File",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if selected_file:
            self.input_file_path = selected_file
            self.file_var.set(os.path.basename(selected_file))

    def extract_emails(self):
        """Reads input file, extracts unique emails using Regex, and saves to file."""
        if not self.input_file_path:
            messagebox.showwarning("Missing Input", "Please select a .txt file first.")
            return

        out_name = self.output_file_var.get().strip()
        if not out_name:
            messagebox.showwarning("Missing Output Name", "Please specify output file name.")
            return

        if not out_name.endswith('.txt'):
            out_name += '.txt'

        try:
            # 1. Read input text file
            with open(self.input_file_path, "r", encoding="utf-8", errors="ignore") as file:
                content = file.read()

            # 2. Regular Expression for emails
            email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            emails = re.findall(email_pattern, content)

            # Remove duplicate emails while preserving order
            unique_emails = list(dict.fromkeys(emails))

            if not unique_emails:
                messagebox.showinfo("No Emails Found", "No valid email addresses were found in the file.")
                self.status_label.config(text="Status: 0 emails found.")
                return

            # 3. Save extracted emails to output file (same directory as source file)
            output_dir = os.path.dirname(self.input_file_path)
            output_file_path = os.path.join(output_dir, out_name)

            with open(output_file_path, "w", encoding="utf-8") as out_file:
                for email in unique_emails:
                    out_file.write(email + "\n")

            self.status_label.config(text=f"Status: Extracted {len(unique_emails)} email(s).")
            messagebox.showinfo(
                "Success",
                f"Done! Found {len(unique_emails)} email(s).\nSaved to: {out_name}"
            )

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
            self.status_label.config(text="Status: Extraction failed.")


if __name__ == "__main__":
    root = tk.Tk()
    app = EmailExtractorApp(root)
    root.mainloop()