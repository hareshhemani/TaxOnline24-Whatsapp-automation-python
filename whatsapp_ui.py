import pandas as pd
import pyautogui
import pyperclip
import time
import random
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from datetime import datetime
import threading
from PIL import Image, ImageTk, ImageDraw
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Appearance Settings
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue") # We will use custom colors anyway

class PremiumWhatsAppUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("TaxOnline24.in - Enterprise WhatsApp Engine")
        self.geometry("1100x750")
        
        # Logic Variables
        self.excel_path = ""
        self.is_running = False
        self.total_count = 0
        self.sent_count = 0
        self.failed_count = 0

        # --- Background Image Implementation ---
        self.bg_image_path = resource_path("bg.png")
        if os.path.exists(self.bg_image_path):
            self.bg_image = Image.open(self.bg_image_path)
            self.bg_photo = ImageTk.PhotoImage(self.bg_image.resize((1100, 750)))
            self.bg_label = tk.Label(self, image=self.bg_photo)
            self.bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # --- Glassmorphism Container ---
        # Main Layout: 2 Columns (Sidebar + Main)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar with "Glass" effect
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=20, fg_color=("#1A1A1A", "#141414"))
        self.sidebar.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="nsew")
        self.sidebar.grid_propagate(False)

        # Sidebar Branding
        self.logo_label = ctk.CTkLabel(self.sidebar, text="TaxOnline24.in", font=ctk.CTkFont(family="Inter", size=22, weight="bold"), text_color="#25D366")
        self.logo_label.pack(pady=(40, 5))
        self.sub_logo = ctk.CTkLabel(self.sidebar, text="AUTOMATION ENGINE", font=ctk.CTkFont(size=10), text_color="#707070")
        self.sub_logo.pack(pady=(0, 30))

        # Action Buttons in Sidebar
        self.btn_browse = ctk.CTkButton(self.sidebar, text="📂 SELECT CONTACTS", font=ctk.CTkFont(weight="bold"),
                                       height=45, fg_color="#333333", hover_color="#444444", command=self.browse_file)
        self.btn_browse.pack(padx=30, pady=10, fill="x")

        self.lbl_file = ctk.CTkLabel(self.sidebar, text="No file loaded", font=ctk.CTkFont(size=11), text_color="gray", wraplength=200)
        self.lbl_file.pack(pady=5)

        # Statistics Section
        self.stats_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.stats_frame.pack(pady=(50, 0), padx=20, fill="x")

        self.create_stat_widget("Total Contacts", "0", "total")
        self.create_stat_widget("Messages Sent", "0", "sent", text_color="#25D366")
        self.create_stat_widget("Process Status", "Idle", "status", text_color="#FFB800")

        # --- Main Dashboard Area ---
        self.dashboard = ctk.CTkFrame(self, corner_radius=20, fg_color=("#F0F0F0", "#191919"))
        self.dashboard.grid(row=0, column=1, padx=(10, 20), pady=20, sticky="nsew")
        self.dashboard.grid_columnconfigure(0, weight=1)
        self.dashboard.grid_rowconfigure(1, weight=1)

        # Header
        self.header = ctk.CTkLabel(self.dashboard, text="Campaign Designer", font=ctk.CTkFont(size=20, weight="bold"))
        self.header.grid(row=0, column=0, padx=30, pady=(30, 10), sticky="w")

        # Message Card
        self.msg_card = ctk.CTkFrame(self.dashboard, fg_color="#282828", corner_radius=15)
        self.msg_card.grid(row=1, column=0, padx=30, pady=10, sticky="nsew")
        self.msg_card.grid_columnconfigure(0, weight=1)
        self.msg_card.grid_rowconfigure(1, weight=1)

        self.msg_label = ctk.CTkLabel(self.msg_card, text="Message Template", font=ctk.CTkFont(size=13, weight="bold"), text_color="#AAAAAA")
        self.msg_label.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="w")

        self.txt_message = ctk.CTkTextbox(self.msg_card, font=ctk.CTkFont(family="Segoe UI", size=14),
                                        fg_color="transparent", border_width=1, border_color="#444444")
        self.txt_message.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.txt_message.insert("0.0", "Namaste {name},\n\nWe are pleased to inform you that your compliance task is ready.\n\nRegards,\nTaxOnline24.in Team")

        # Controls & Progress
        self.footer = ctk.CTkFrame(self.dashboard, fg_color="transparent")
        self.footer.grid(row=2, column=0, padx=30, pady=(10, 30), sticky="ew")
        self.footer.grid_columnconfigure(0, weight=1)

        # Progress Bar with Gradient look (using custom color)
        self.progress_bar = ctk.CTkProgressBar(self.footer, height=12, progress_color="#25D366", fg_color="#333333")
        self.progress_bar.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        self.progress_bar.set(0)

        self.btn_start = ctk.CTkButton(self.footer, text="🚀 LAUNCH CAMPAIGN", font=ctk.CTkFont(size=16, weight="bold"),
                                      height=55, fg_color="#25D366", hover_color="#1DA851", command=self.start_thread)
        self.btn_start.grid(row=1, column=0, sticky="ew")

        # Log View (Floating)
        self.log_container = ctk.CTkFrame(self.dashboard, height=120, fg_color="#0A0A0A", corner_radius=10)
        self.log_container.grid(row=3, column=0, padx=30, pady=(0, 30), sticky="ew")
        self.log_container.grid_columnconfigure(0, weight=1)
        
        self.log_box = ctk.CTkTextbox(self.log_container, height=80, fg_color="transparent", font=ctk.CTkFont(family="Consolas", size=11), text_color="#00FF41")
        self.log_box.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        self.log_box.configure(state="disabled")

    def create_stat_widget(self, label, value, key, text_color="white"):
        frame = ctk.CTkFrame(self.stats_frame, fg_color="#3C3C3C", height=70, corner_radius=10)
        frame.pack(pady=5, fill="x")
        frame.pack_propagate(False)
        
        lbl = ctk.CTkLabel(frame, text=label, font=ctk.CTkFont(size=11), text_color="#888888")
        lbl.pack(pady=(10, 0))
        
        val = ctk.CTkLabel(frame, text=value, font=ctk.CTkFont(size=18, weight="bold"), text_color=text_color)
        val.pack(pady=(0, 5))
        
        setattr(self, f"stat_{key}", val)

    def add_log(self, message):
        self.log_box.configure(state="normal")
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_box.insert("end", f"> [{ts}] {message}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def browse_file(self):
        self.excel_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if self.excel_path:
            filename = os.path.basename(self.excel_path)
            self.lbl_file.configure(text=f"📄 {filename}", text_color="#25D366")
            try:
                df = pd.read_excel(self.excel_path)
                self.total_count = len(df)
                self.stat_total.configure(text=str(self.total_count))
                self.add_log(f"Loaded {self.total_count} contacts.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read Excel: {e}")

    def start_thread(self):
        if not self.excel_path:
            messagebox.showerror("Error", "Select contacts first!")
            return
        if self.is_running: return

        msg = self.txt_message.get("1.0", "end-1c").strip()
        if not msg:
            messagebox.showerror("Error", "Message cannot be empty!")
            return

        self.is_running = True
        self.btn_start.configure(state="disabled", text="ENGINE RUNNING...", fg_color="#555555")
        self.stat_status.configure(text="Active", text_color="#25D366")
        threading.Thread(target=self.run_automation, daemon=True).start()

    def run_automation(self):
        msg_template = self.txt_message.get("1.0", "end-1c").strip()
        
        try:
            df = pd.read_excel(self.excel_path)
            if 'mobile' not in df.columns or 'name' not in df.columns:
                messagebox.showerror("Error", "Columns 'name' and 'mobile' required!")
                return
            
            self.add_log("System warming up... 10s delay.")
            time.sleep(10)

            for index, row in df.iterrows():
                name = str(row['name']).strip()
                number = str(row['mobile']).strip()
                custom_message = msg_template.replace("{name}", name)

                # --- Core Automation Logic (Enhanced Safety) ---
                # 1. Clear everything first
                pyautogui.press('esc') 
                time.sleep(0.5)
                pyautogui.press('esc')
                time.sleep(0.5)

                # 2. Open Search
                pyautogui.hotkey('ctrl', 'alt', '/')
                time.sleep(1)
                
                # 3. Clear search bar and type number
                for _ in range(15): pyautogui.press('backspace')
                pyautogui.typewrite(number)
                
                # 4. Wait for results and try to select
                time.sleep(random.uniform(4, 6))
                pyautogui.press('enter')
                time.sleep(2)
                
                # 5. Paste and Send
                pyperclip.copy(custom_message)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(1)
                pyautogui.press('enter')

                # UI Feedback
                self.sent_count += 1
                self.stat_sent.configure(text=str(self.sent_count))
                progress = (index + 1) / self.total_count
                self.progress_bar.set(progress)
                self.add_log(f"Processed: {name}")
                
                # Update DataFrame Status
                df.at[index, 'Status'] = 'Processed'
                
                # Safety Delay
                if index < self.total_count - 1:
                    delay = random.uniform(20, 40)
                    self.add_log(f"Cooldown: {int(delay)}s")
                    time.sleep(delay)

            report = f"Report_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
            df.to_excel(report, index=False)
            self.add_log(f"Campaign Complete. Report: {report}")
            messagebox.showinfo("Success", "Campaign successfully finished!")

        except Exception as e:
            self.add_log(f"CRITICAL ERROR: {str(e)}")
            messagebox.showerror("System Error", str(e))
        
        finally:
            self.is_running = False
            self.btn_start.configure(state="normal", text="🚀 LAUNCH CAMPAIGN", fg_color="#25D366")
            self.stat_status.configure(text="Completed", text_color="#FFB800")

if __name__ == "__main__":
    app = PremiumWhatsAppUI()
    # Handle window resize for background
    def on_resize(event):
        if event.widget == app:
            new_w, new_h = event.width, event.height
            resized_bg = app.bg_image.resize((new_w, new_h))
            app.bg_photo = ImageTk.PhotoImage(resized_bg)
            app.bg_label.configure(image=app.bg_photo)
    
    app.bind("<Configure>", on_resize)
    app.mainloop()
