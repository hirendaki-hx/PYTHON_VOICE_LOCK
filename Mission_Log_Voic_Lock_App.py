import os
import sys
import threading
import speech_recognition    as sr
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter.scrolledtext import ScrolledText

PASS_PHRASE = "open diary"
MISSION_LOG_FILE = "agent_logs.txt"

class MissionLogApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mission Log System v1.0")
        self.geometry("600x400")
        self.resizable(False, False)
        self.authenticated = False
        self.create_widgets()

    def create_widgets(self):
        self.status_label = tk.Label(self, text="Status: Locked", font=(None, 12))
        self.status_label.pack(pady=10)
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=5)
        self.auth_btn = tk.Button(btn_frame, text="Authenticate (Voice)", width=18, command=self.start_auth_thread)
        self.auth_btn.grid(row=0, column=0, padx=5)
        self.log_btn = tk.Button(btn_frame, text="Log New Report", width=18, state=tk.DISABLED, command=self.store_report)
        self.log_btn.grid(row=0, column=1, padx=5)
        self.review_btn = tk.Button(btn_frame, text="Review Logs", width=18, state=tk.DISABLED, command=self.review_logs)
        self.review_btn.grid(row=0, column=2, padx=5)
        self.exit_btn = tk.Button(self, text="Exit", width=10, command=self.exit_app)
        self.exit_btn.pack(pady=8)
        self.log_display = ScrolledText(self, wrap=tk.WORD, height=15)
        self.log_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.log_display.configure(state=tk.DISABLED)

    def start_auth_thread(self):
        thread = threading.Thread(target=self.authenticate)
        thread.daemon = True
        thread.start()

    def authenticate(self):
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            text = recognizer.recognize_google(audio).lower()
            if text == PASS_PHRASE:
                self.authenticated = True
                self.after(0, lambda: self.update_ui_authenticated())
                self.after(0, lambda: messagebox.showinfo("Authentication", "Authentication successful"))
            else:
                self.after(0, lambda: messagebox.showerror("Authentication", "Incorrect passphrase. Access Denied."))
        except sr.UnknownValueError:
            self.after(0, lambda: messagebox.showwarning("Authentication", "Could not understand audio."))
        except sr.WaitTimeoutError:
            self.after(0, lambda: messagebox.showwarning("Authentication", "No speech detected."))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Authentication", f"Error occurred: {e}"))

    def update_ui_authenticated(self):
        self.status_label.config(text="Status: Unlocked")
        self.log_btn.config(state=tk.NORMAL)
        self.review_btn.config(state=tk.NORMAL)
        self.auth_btn.config(state=tk.DISABLED)

    def store_report(self):
        report = simpledialog.askstring("New Report", "Enter mission report (leave empty to cancel):", parent=self)
        if not report or not report.strip():
            messagebox.showinfo("Report", "Empty report not saved.")
            return
        try:
            with open(MISSION_LOG_FILE, "a", encoding="utf-8") as file:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                file.write(f"[{timestamp}]\n{report}\n---\n")
            messagebox.showinfo("Report", "Report saved successfully!")
        except Exception as e:
            messagebox.showerror("Report", f"Failed to save report: {e}")

    def review_logs(self):
        if os.path.exists(MISSION_LOG_FILE):
            try:
                with open(MISSION_LOG_FILE, "r", encoding="utf-8") as file:
                    content = file.read().strip()
                if not content:
                    content = "No mission logs found."
            except Exception as e:
                content = f"Failed to load logs: {e}"
        else:
            content = "No mission logs found."
        self.log_display.configure(state=tk.NORMAL)
        self.log_display.delete(1.0, tk.END)
        self.log_display.insert(tk.END, content)
        self.log_display.configure(state=tk.DISABLED)

    def exit_app(self):
        self.destroy()

if __name__ == "__main__":
    app = MissionLogApp()
    app.mainloop()
