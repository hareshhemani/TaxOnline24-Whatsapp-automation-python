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
from PIL import Image, ImageTk
import os
import sys
import struct
import io
import win32clipboard
import win32con

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def copy_to_clipboard(filepath):
    """
    Copies an image or document to Windows clipboard using native Windows formats.
    Supports CF_DIB (bitmap) and CF_HDROP (file drop) for full WhatsApp Web compatibility.
    """
    abs_path = os.path.abspath(filepath)
    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"Attachment file not found: {abs_path}")

    ext = os.path.splitext(abs_path)[1].lower()
    is_image = ext in ['.png', '.jpg', '.jpeg', '.bmp', '.webp']

    # 1. Build CF_HDROP structure (File Drop List)
    offset = 20
    header = struct.pack('IIIII', offset, 0, 0, 0, 1)
    files_bytes = (abs_path + '\0\0').encode('utf-16le')
    hdrop_data = header + files_bytes

    win32clipboard.OpenClipboard()
    try:
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_HDROP, hdrop_data)

        # For images, also provide CF_DIB bitmap data for immediate browser inline paste
        if is_image:
            try:
                img = Image.open(abs_path)
                output = io.BytesIO()
                img.convert("RGB").save(output, "BMP")
                dib_data = output.getvalue()[14:]  # Strip 14-byte BMP header
                output.close()
                win32clipboard.SetClipboardData(win32clipboard.CF_DIB, dib_data)
            except Exception:
                pass
    finally:
        win32clipboard.CloseClipboard()

def is_search_bar_still_active(number):
    """
    Detects if focus is still trapped inside the search bar containing the phone number.
    If chat was opened, the active field is the empty message input box, not the search bar.
    """
    clean_num = ''.join(c for c in str(number) if c.isdigit())
    if not clean_num:
        return False
        
    sentinel = f"__WA_SENTINEL_{random.randint(10000, 99999)}__"
    pyperclip.copy(sentinel)
    time.sleep(0.2)
    
    # Try selecting and copying content of currently active field
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.25)
    
    copied = pyperclip.paste().strip()
    
    # If clipboard was NOT overwritten by Ctrl+C, the active input box was EMPTY (chat is open!)
    if copied == sentinel:
        return False
        
    clean_copied = ''.join(c for c in copied if c.isdigit())
    
    # If copied text matches digits of searched phone number, search bar is definitely still active!
    if len(clean_copied) >= 7:
        if clean_num in clean_copied or clean_copied in clean_num or clean_num[-7:] in clean_copied:
            return True
        
    return False

# Appearance Settings
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class PremiumWhatsAppUIv2(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("TaxOnline24 - Enterprise WhatsApp Engine v2.0 (Attachments & Media)")
        self.geometry("1150x800")
        self.minsize(1050, 720)
        
        # Logic Variables
        self.excel_path = ""
        self.attachment_path = ""
        self.is_running = False
        self.total_count = 0
        self.sent_count = 0
        self.failed_count = 0
        self.last_resized_size = (1150, 800)

        # --- Background Image Implementation ---
        self.bg_image_path = resource_path("bg.png")
        if not os.path.exists(self.bg_image_path):
            parent_bg = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "bg.png")
            if os.path.exists(parent_bg):
                self.bg_image_path = parent_bg

        if os.path.exists(self.bg_image_path):
            self.bg_image = Image.open(self.bg_image_path)
            self.bg_photo = ImageTk.PhotoImage(self.bg_image.resize((1150, 800)))
            self.bg_label = tk.Label(self, image=self.bg_photo)
            self.bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # --- Glassmorphism Container ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar with "Glass" effect
        self.sidebar = ctk.CTkFrame(self, width=300, corner_radius=20, fg_color=("#1A1A1A", "#141414"))
        self.sidebar.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="nsew")
        self.sidebar.grid_propagate(False)

        # Sidebar Branding
        self.logo_label = ctk.CTkLabel(self.sidebar, text="TaxOnline24", font=ctk.CTkFont(family="Inter", size=22, weight="bold"), text_color="#25D366")
        self.logo_label.pack(pady=(20, 2))
        self.sub_logo = ctk.CTkLabel(self.sidebar, text="AUTOMATION ENGINE v2.0", font=ctk.CTkFont(size=10, weight="bold"), text_color="#707070")
        self.sub_logo.pack(pady=(0, 15))

        # --- Contact Selection ---
        self.btn_browse = ctk.CTkButton(self.sidebar, text="📂 SELECT CONTACTS", font=ctk.CTkFont(weight="bold"),
                                       height=38, fg_color="#333333", hover_color="#444444", command=self.browse_file)
        self.btn_browse.pack(padx=25, pady=4, fill="x")

        self.lbl_file = ctk.CTkLabel(self.sidebar, text="No contacts loaded", font=ctk.CTkFont(size=11), text_color="gray", wraplength=250)
        self.lbl_file.pack(pady=(2, 8))

        # --- Attachment Selection (New in v2.0) ---
        self.btn_attach = ctk.CTkButton(self.sidebar, text="📎 ATTACH IMAGE / DOC", font=ctk.CTkFont(weight="bold"),
                                        height=38, fg_color="#2A4B7C", hover_color="#365C96", command=self.browse_attachment)
        self.btn_attach.pack(padx=25, pady=4, fill="x")

        self.lbl_attachment = ctk.CTkLabel(self.sidebar, text="No attachment (Text only)", font=ctk.CTkFont(size=11), text_color="gray", wraplength=250)
        self.lbl_attachment.pack(pady=(2, 2))

        self.btn_clear_attach = ctk.CTkButton(self.sidebar, text="❌ Remove Attachment", font=ctk.CTkFont(size=10),
                                              height=24, fg_color="transparent", text_color="#FF6B6B", hover_color="#331A1A",
                                              command=self.clear_attachment)
        self.btn_clear_attach.pack(pady=(0, 10))
        self.btn_clear_attach.configure(state="disabled")

        # Statistics Section
        self.stats_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.stats_frame.pack(pady=(5, 0), padx=20, fill="x")

        self.create_stat_widget("Total Contacts", "0", "total")
        self.create_stat_widget("Messages Sent", "0", "sent", text_color="#25D366")
        self.create_stat_widget("Failed / Not Found", "0", "failed", text_color="#FF5555")
        self.create_stat_widget("Process Status", "Idle", "status", text_color="#FFB800")

        # --- Main Dashboard Area ---
        self.dashboard = ctk.CTkFrame(self, corner_radius=20, fg_color=("#F0F0F0", "#191919"))
        self.dashboard.grid(row=0, column=1, padx=(10, 20), pady=20, sticky="nsew")
        self.dashboard.grid_columnconfigure(0, weight=1)
        self.dashboard.grid_rowconfigure(1, weight=1)

        # Header
        self.header_frame = ctk.CTkFrame(self.dashboard, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=30, pady=(20, 5), sticky="ew")
        
        self.header = ctk.CTkLabel(self.header_frame, text="Campaign Designer (v2.0 Attachments)", font=ctk.CTkFont(size=20, weight="bold"))
        self.header.pack(side="left")

        self.mode_badge = ctk.CTkLabel(self.header_frame, text="TEXT MODE", font=ctk.CTkFont(size=11, weight="bold"),
                                       fg_color="#333333", text_color="#AAAAAA", corner_radius=6, padx=10, pady=2)
        self.mode_badge.pack(side="right")

        # Message Card
        self.msg_card = ctk.CTkFrame(self.dashboard, fg_color="#282828", corner_radius=15)
        self.msg_card.grid(row=1, column=0, padx=30, pady=10, sticky="nsew")
        self.msg_card.grid_columnconfigure(0, weight=1)
        self.msg_card.grid_rowconfigure(1, weight=1)

        self.msg_info_frame = ctk.CTkFrame(self.msg_card, fg_color="transparent")
        self.msg_info_frame.grid(row=0, column=0, padx=20, pady=(12, 4), sticky="ew")

        self.msg_label = ctk.CTkLabel(self.msg_info_frame, text="Message / Caption Template", font=ctk.CTkFont(size=13, weight="bold"), text_color="#AAAAAA")
        self.msg_label.pack(side="left")

        self.caption_hint = ctk.CTkLabel(self.msg_info_frame, text="* Supports {name} placeholder. Acts as caption when attachment is used.",
                                         font=ctk.CTkFont(size=11), text_color="#777777")
        self.caption_hint.pack(side="right")

        self.txt_message = ctk.CTkTextbox(self.msg_card, font=ctk.CTkFont(family="Segoe UI", size=14),
                                         fg_color="transparent", border_width=1, border_color="#444444")
        self.txt_message.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="nsew")
        self.txt_message.insert("0.0", "Namaste {name},\n\nPlease find the attached document for your review.\n\nRegards,\nTaxOnline24 Team")

        # Controls & Progress
        self.footer = ctk.CTkFrame(self.dashboard, fg_color="transparent")
        self.footer.grid(row=2, column=0, padx=30, pady=(5, 15), sticky="ew")
        self.footer.grid_columnconfigure(0, weight=1)

        # Progress Bar
        self.progress_bar = ctk.CTkProgressBar(self.footer, height=12, progress_color="#25D366", fg_color="#333333")
        self.progress_bar.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        self.progress_bar.set(0)

        # Launch / Stop Button
        self.btn_start = ctk.CTkButton(self.footer, text="🚀 LAUNCH CAMPAIGN", font=ctk.CTkFont(size=16, weight="bold"),
                                      height=50, fg_color="#25D366", hover_color="#1DA851", command=self.handle_button_click)
        self.btn_start.grid(row=1, column=0, sticky="ew")

        # Log View
        self.log_container = ctk.CTkFrame(self.dashboard, height=110, fg_color="#0A0A0A", corner_radius=10)
        self.log_container.grid(row=3, column=0, padx=30, pady=(0, 20), sticky="ew")
        self.log_container.grid_columnconfigure(0, weight=1)
        
        self.log_box = ctk.CTkTextbox(self.log_container, height=85, fg_color="transparent", font=ctk.CTkFont(family="Consolas", size=11), text_color="#00FF41")
        self.log_box.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        self.log_box.configure(state="disabled")

    def create_stat_widget(self, label, value, key, text_color="white"):
        frame = ctk.CTkFrame(self.stats_frame, fg_color="#2C2C2C", height=54, corner_radius=8)
        frame.pack(pady=3, fill="x")
        frame.pack_propagate(False)
        
        lbl = ctk.CTkLabel(frame, text=label, font=ctk.CTkFont(size=10), text_color="#888888")
        lbl.pack(pady=(4, 0))
        
        val = ctk.CTkLabel(frame, text=value, font=ctk.CTkFont(size=16, weight="bold"), text_color=text_color)
        val.pack(pady=(0, 4))
        
        setattr(self, f"stat_{key}", val)

    def add_log(self, message):
        def _append():
            self.log_box.configure(state="normal")
            ts = datetime.now().strftime("%H:%M:%S")
            self.log_box.insert("end", f"> [{ts}] {message}\n")
            self.log_box.see("end")
            self.log_box.configure(state="disabled")
        self.after(0, _append)

    def browse_file(self):
        self.excel_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if self.excel_path:
            filename = os.path.basename(self.excel_path)
            self.lbl_file.configure(text=f"📄 {filename}", text_color="#25D366")
            try:
                df = pd.read_excel(self.excel_path)
                self.total_count = len(df)
                self.stat_total.configure(text=str(self.total_count))
                has_att_col = 'attachment' in df.columns
                att_note = " (Has 'attachment' column)" if has_att_col else ""
                self.add_log(f"Loaded {self.total_count} contacts{att_note}.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read Excel: {e}")

    def browse_attachment(self):
        filetypes = [
            ("All Supported Attachments", "*.png *.jpg *.jpeg *.bmp *.webp *.pdf *.docx *.xlsx *.txt *.zip *.csv"),
            ("Images", "*.png *.jpg *.jpeg *.bmp *.webp"),
            ("Documents (PDF/Office)", "*.pdf *.docx *.xlsx *.txt *.csv *.zip"),
            ("All Files", "*.*")
        ]
        chosen = filedialog.askopenfilename(filetypes=filetypes)
        if chosen:
            self.attachment_path = chosen
            filename = os.path.basename(chosen)
            ext = os.path.splitext(chosen)[1].lower()
            
            if ext in ['.png', '.jpg', '.jpeg', '.bmp', '.webp']:
                icon = "🖼️ Image"
            elif ext == '.pdf':
                icon = "📕 PDF"
            elif ext in ['.xlsx', '.xls', '.csv']:
                icon = "📊 Excel"
            elif ext in ['.docx', '.doc']:
                icon = "📄 Word"
            else:
                icon = "📎 Doc"

            self.lbl_attachment.configure(text=f"{icon}: {filename}", text_color="#4FC3F7")
            self.btn_clear_attach.configure(state="normal")
            self.mode_badge.configure(text="ATTACHMENT MODE", fg_color="#1E4620", text_color="#25D366")
            self.add_log(f"Attachment selected: {filename}")

    def clear_attachment(self):
        self.attachment_path = ""
        self.lbl_attachment.configure(text="No attachment (Text only)", text_color="gray")
        self.btn_clear_attach.configure(state="disabled")
        self.mode_badge.configure(text="TEXT MODE", fg_color="#333333", text_color="#AAAAAA")
        self.add_log("Attachment cleared. Reverted to Text-only mode.")

    def handle_button_click(self):
        if self.is_running:
            # User wants to stop running campaign
            self.is_running = False
            self.add_log("⚠️ Stopping campaign safely... finishing current task.")
            self.btn_start.configure(text="STOPPING...", fg_color="#777777", state="disabled")
        else:
            self.start_thread()

    def start_thread(self):
        if not self.excel_path:
            messagebox.showerror("Error", "Select contacts first!")
            return

        msg = self.txt_message.get("1.0", "end-1c").strip()
        if not msg and not self.attachment_path:
            messagebox.showerror("Error", "Message or Attachment is required!")
            return

        self.is_running = True
        self.sent_count = 0
        self.failed_count = 0
        self.stat_sent.configure(text="0")
        self.stat_failed.configure(text="0")
        self.progress_bar.set(0)
        self.btn_start.configure(text="🛑 STOP CAMPAIGN", fg_color="#D32F2F", hover_color="#B71C1C", state="normal")
        self.stat_status.configure(text="Active", text_color="#25D366")
        threading.Thread(target=self.run_automation, daemon=True).start()

    def run_automation(self):
        msg_template = self.txt_message.get("1.0", "end-1c").strip()
        
        try:
            df = pd.read_excel(self.excel_path)
            if 'mobile' not in df.columns or 'name' not in df.columns:
                self.after(0, lambda: messagebox.showerror("Error", "Columns 'name' and 'mobile' required in Excel sheet!"))
                return
            
            has_attachment_col = 'attachment' in df.columns
            self.add_log("System warming up... 10s delay. Please focus WhatsApp Web.")
            
            for _ in range(10):
                if not self.is_running:
                    self.add_log("Campaign stopped during warmup.")
                    return
                time.sleep(1)

            for index, row in df.iterrows():
                if not self.is_running:
                    self.add_log("🛑 Campaign safely stopped by user.")
                    break

                name = str(row['name']).strip()
                
                # Sanitize phone number (remove .0 float artifacts, spaces, dashes)
                raw_num = str(row['mobile']).strip()
                if raw_num.endswith('.0'):
                    raw_num = raw_num[:-2]
                number = ''.join(c for c in raw_num if c.isdigit() or c == '+')

                # Smart Country Code Check: If 10-digit Indian mobile starting with 6-9, prefix '91'
                if len(number) == 10 and number[0] in '6789':
                    number = '91' + number

                custom_message = msg_template.replace("{name}", name)

                # Determine active attachment (Row-specific column overrides GUI selection)
                target_attachment = None
                if has_attachment_col and pd.notna(row['attachment']):
                    candidate = str(row['attachment']).strip()
                    if os.path.exists(candidate):
                        target_attachment = candidate
                    else:
                        excel_dir = os.path.dirname(os.path.abspath(self.excel_path))
                        rel_path = os.path.join(excel_dir, candidate)
                        if os.path.exists(rel_path):
                            target_attachment = rel_path

                if not target_attachment and self.attachment_path and os.path.exists(self.attachment_path):
                    target_attachment = self.attachment_path

                # --- STEP 1: Clear Search / Popups ---
                pyautogui.press('esc') 
                time.sleep(0.3)
                pyautogui.press('esc')
                time.sleep(0.3)

                # --- STEP 2: Open Search Bar in WhatsApp Web ---
                pyautogui.hotkey('ctrl', 'alt', '/')
                time.sleep(0.8)
                
                # --- STEP 3: Clear Search Box & Type Recipient Number ---
                pyautogui.hotkey('ctrl', 'a')
                pyautogui.press('backspace')
                time.sleep(0.3)
                pyautogui.typewrite(number)
                
                # --- STEP 4: Wait for Search Query to Resolve ---
                time.sleep(random.uniform(3.5, 4.5))
                
                # Try opening chat (Enter)
                pyautogui.press('enter')
                time.sleep(1.5)

                # If still in search bar, retry Enter once (NEVER press Down Arrow - it selects the wrong first chat!)
                if is_search_bar_still_active(number):
                    pyautogui.press('enter')
                    time.sleep(1.5)

                # --- STEP 5: Verification (Did the chat open?) ---
                if is_search_bar_still_active(number):
                    # Number is NOT registered on WhatsApp or contact was not found!
                    # Safely skip to prevent sending to the wrong / first chat in the list.
                    self.add_log(f"⚠️ NOT FOUND / NOT ON WHATSAPP: {name} ({number}) - Skipping")
                    df.at[index, 'Status'] = 'Failed (Not on WhatsApp / Not Found)'
                    df.at[index, 'Attachment_Sent'] = 'None'
                    
                    self.failed_count += 1
                    self.stat_failed.configure(text=str(self.failed_count))

                    # CRITICAL: Clean the search bar completely so it does not interfere with next contact
                    pyautogui.press('esc')
                    time.sleep(0.3)
                    pyautogui.hotkey('ctrl', 'a')
                    pyautogui.press('backspace')
                    time.sleep(0.3)
                    pyautogui.press('esc')
                    time.sleep(0.5)

                    # Update progress bar
                    progress = (index + 1) / self.total_count
                    self.progress_bar.set(progress)

                    # Safety Cooldown before moving to next contact
                    if index < self.total_count - 1 and self.is_running:
                        time.sleep(random.uniform(2, 4))
                    continue

                # --- STEP 6: Chat Opened Successfully! Send Content ---
                if target_attachment and os.path.exists(target_attachment):
                    # --- ATTACHMENT MODE ---
                    att_name = os.path.basename(target_attachment)
                    self.add_log(f"Pasting attachment for {name}: {att_name}")
                    
                    # Copy attachment to Windows clipboard
                    copy_to_clipboard(target_attachment)
                    time.sleep(0.5)

                    # Trigger paste in WhatsApp Web chat
                    pyautogui.hotkey('ctrl', 'v')

                    # Wait for media preview popup to appear
                    time.sleep(3.5)

                    # Paste customized caption text if present
                    if custom_message:
                        pyperclip.copy(custom_message)
                        pyautogui.hotkey('ctrl', 'v')
                        time.sleep(1.0)

                    # Send attachment + caption:
                    # Dual method: Try locating visual Send button on screen first, fallback to Enter
                    sent_via_click = False
                    script_dir = os.path.dirname(os.path.abspath(__file__))
                    send_btn_icon = os.path.join(script_dir, "send_button.png")
                    if not os.path.exists(send_btn_icon):
                        send_btn_icon = resource_path("send_button.png")

                    if os.path.exists(send_btn_icon):
                        try:
                            btn_pos = pyautogui.locateCenterOnScreen(send_btn_icon, confidence=0.8)
                            if btn_pos:
                                pyautogui.click(btn_pos)
                                sent_via_click = True
                                time.sleep(1.0)
                        except Exception:
                            pass

                    if not sent_via_click:
                        pyautogui.press('enter')

                    time.sleep(3.5)  # Wait buffer for file upload initiation
                    df.at[index, 'Status'] = 'Sent with Attachment'
                    df.at[index, 'Attachment_Sent'] = att_name

                else:
                    # --- TEXT ONLY MODE ---
                    pyperclip.copy(custom_message)
                    pyautogui.hotkey('ctrl', 'v')
                    time.sleep(1.0)
                    pyautogui.press('enter')
                    df.at[index, 'Status'] = 'Sent (Text)'
                    df.at[index, 'Attachment_Sent'] = 'None'

                # UI Feedback
                self.sent_count += 1
                self.stat_sent.configure(text=str(self.sent_count))
                progress = (index + 1) / self.total_count
                self.progress_bar.set(progress)
                self.add_log(f"✅ Processed & Sent: {name} ({number})")
                
                # Safety Cooldown between messages
                if index < self.total_count - 1 and self.is_running:
                    delay = random.uniform(20, 38)
                    self.add_log(f"Cooldown: {int(delay)}s for safety...")
                    # Allow cancellation during cooldown
                    cooldown_end = time.time() + delay
                    while time.time() < cooldown_end and self.is_running:
                        time.sleep(0.5)

            # Export Detailed Audit Report
            report = f"Report_v2_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
            df.to_excel(report, index=False)
            self.add_log(f"Campaign Complete! Sent: {self.sent_count}, Failed: {self.failed_count}")
            self.add_log(f"Report saved: {report}")
            
            completion_msg = f"Campaign finished!\n\nSent: {self.sent_count}\nFailed / Not on WhatsApp: {self.failed_count}\n\nReport saved to: {report}"
            self.after(0, lambda: messagebox.showinfo("Summary", completion_msg))

        except Exception as e:
            self.add_log(f"CRITICAL ERROR: {str(e)}")
            err_msg = str(e)
            self.after(0, lambda: messagebox.showerror("System Error", err_msg))
        
        finally:
            self.is_running = False
            self.btn_start.configure(state="normal", text="🚀 LAUNCH CAMPAIGN", fg_color="#25D366", hover_color="#1DA851")
            self.stat_status.configure(text="Completed", text_color="#FFB800")

if __name__ == "__main__":
    app = PremiumWhatsAppUIv2()
    
    # Optimized window resize handler with debounce
    def on_resize(event):
        if event.widget == app and hasattr(app, 'bg_image'):
            new_w, new_h = event.width, event.height
            old_w, old_h = app.last_resized_size
            if abs(new_w - old_w) > 25 or abs(new_h - old_h) > 25:
                if new_w > 100 and new_h > 100:
                    app.last_resized_size = (new_w, new_h)
                    resized_bg = app.bg_image.resize((new_w, new_h))
                    app.bg_photo = ImageTk.PhotoImage(resized_bg)
                    app.bg_label.configure(image=app.bg_photo)
    
    app.bind("<Configure>", on_resize)
    app.mainloop()
