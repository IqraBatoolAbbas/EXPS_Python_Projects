import os
import re
import ctypes
import requests
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


class WebTitleScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Automated Webpage Title Scraper")
        self.root.geometry("640x420")
        self.root.resizable(False, False)
        self.root.configure(bg="#ffffff")

        # Title Header
        title_label = tk.Label(
            root,
            text="🌐 Webpage Title Scraper",
            font=("Segoe UI", 18, "bold"),
            bg="#ffffff",
            fg="#1a1a1a"
        )
        title_label.pack(pady=(20, 15))

        # 1. Webpage URL Input Row
        self.url_var = tk.StringVar(value="https://www.google.com")
        self.create_input_row(
            "Target Webpage URL:",
            self.url_var,
            placeholder="e.g., https://example.com"
        )

        # 2. Save File Name Row
        self.filename_var = tk.StringVar(value="scraped_title.txt")
        self.create_input_row(
            "Save Output File As:",
            self.filename_var,
            placeholder="scraped_title.txt"
        )

        # Process Button
        scrape_btn = tk.Button(
            root,
            text="🚀 Scrape & Save Title",
            font=("Segoe UI", 11, "bold"),
            bg="#0078d4",
            fg="white",
            activebackground="#005a9e",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=15,
            pady=8,
            command=self.scrape_title,
            cursor="hand2"
        )
        scrape_btn.pack(pady=20)

        # Status Label
        self.status_label = tk.Label(
            root,
            text="Status: Ready",
            font=("Segoe UI", 9, "italic"),
            bg="#ffffff",
            fg="#666666"
        )
        self.status_label.pack(side="bottom", pady=12)

    def create_input_row(self, label_text, text_var, placeholder=""):
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

    def scrape_title(self):
        """Fetches webpage content and extracts the webpage title."""
        url = self.url_var.get().strip()
        filename = self.filename_var.get().strip()

        # Input Validations
        if not url:
            messagebox.showwarning("Missing URL", "Please enter a valid webpage URL.")
            return

        if not filename:
            messagebox.showwarning("Missing Filename", "Please enter an output file name.")
            return

        # Ensure URL starts with http:// or https://
        if not (url.startswith("http://") or url.startswith("https://")):
            url = "https://" + url

        if not filename.endswith(".txt"):
            filename += ".txt"

        try:
            self.status_label.config(text="Status: Fetching webpage...")
            self.root.update_idletasks()

            # Set user-agent header to avoid getting blocked by websites
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }

            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            # Extract title using regular expressions
            title_search = re.search(r'<title>(.*?)</title>', response.text, re.IGNORECASE | re.DOTALL)

            if title_search:
                page_title = title_search.group(1).strip()
            else:
                page_title = "No Title Found"

            # Save extracted title to file
            with open(filename, "w", encoding="utf-8") as file:
                file.write(f"URL: {url}\n")
                file.write(f"Extracted Title: {page_title}\n")

            self.status_label.config(text=f"Status: Title saved to '{filename}' successfully.")
            messagebox.showinfo(
                "Success",
                f"Page Title Scraped Successfully!\n\nTitle: {page_title}\nSaved to: {filename}"
            )

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Network Error", f"Failed to fetch webpage:\n{str(e)}")
            self.status_label.config(text="Status: Request failed.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
            self.status_label.config(text="Status: Process failed.")


if __name__ == "__main__":
    root = tk.Tk()
    app = WebTitleScraperApp(root)
    root.mainloop()