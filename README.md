<div align=""center"">

# 🚀 Enterprise WhatsApp Automation Engine
### Modern, Safe & Human-Like Client Communication Suite

[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![GUI Framework](https://img.shields.io/badge/CustomTkinter-Dark%20Glassmorphism-25D366.svg?style=for-the-badge)](https://github.com/TomSchimansky/CustomTkinter)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE.md)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D6.svg?style=for-the-badge&logo=windows)](https://www.microsoft.com/windows)
[![Developer](https://img.shields.io/badge/Author-Haresh%20Kumar%20Hemani-orange.svg?style=for-the-badge)](https://www.taxonline24.in)

<p align=""center"">
  <b>A desktop automation solution built for tax professionals, consultants, and enterprises to send personalized client alerts, compliance notifications, and transactional updates seamlessly via WhatsApp Web.</b>
</p>

[Key Features](#-key-features) •
[Installation](#-installation--setup) •
[Usage Guide](#-how-to-use) •
[Contact Schema](#-excel-contact-format) •
[Executable Build](#-building-standalone-exe) •
[Author & Copyright](#-developer--copyright)

</div>

---

## 🌟 Key Features

- 🎨 **Modern Dark-Themed Glassmorphism UI**:
  - Built with CustomTkinter and Pillow (PIL) for high-DPI scaling and sleek visual ergonomics.
  - Dynamically resizable background asset integration.

- 🤖 **Human-Like Simulation & Account Safety**:
  - Emulates natural operator interactions: search bar activation (Ctrl + Alt + /), backspace clearing, clipboard pasting, and keyboard triggers.
  - **10-Second Warm-up Buffer**: Allows user to comfortably switch focus to WhatsApp Web.
  - **Dynamic Randomized Delay**: Cooldown interval between 20 to 40 seconds per message to comply with safety recommendations and mitigate rate-limiting risks.

- 📑 **Excel-Driven Contact Management**:
  - Supports .xlsx and .xls files.
  - Validates required columns (
ame, mobile) before launching campaigns.

- 💬 **Dynamic Message Personalization**:
  - Write custom message templates with {name} parameter placeholder for 1-to-1 client customization.

- 📊 **Real-Time Live Dashboard & Monitoring**:
  - Live metric cards: Total Contacts Loaded, Messages Sent, and Current Status.
  - Floating green-hacker terminal log box displaying real-time timestamped progress.
  - Responsive visual progress bar.

- 📈 **Audit Trail & Automatic Reporting**:
  - Automatically exports a timestamped completion report (Report_YYYYMMDD_HHMM.xlsx) with delivery statuses.

- 🧵 **Multi-Threaded Engine**:
  - Heavy automation tasks execute on a dedicated background thread, preventing UI freezing or Windows "Not Responding" warnings.

---

## 📁 Repository Structure

```
├── bg.png                 # Background UI asset
├── contacts.xlsx          # Sample contact sheet template
├── whatsapp_ui.py         # Main application GUI & Automation engine
├── requirements.txt       # Python project dependencies
├── .gitignore             # Standard Git ignore configurations
├── LICENSE.md             # MIT License with Copyright & contact info
├── README.md              # Project documentation & guides
└── CONTRIBUTING.md        # Guidelines for contributions
```

---

## ⚙️ Prerequisites & System Requirements

1. **Operating System**: Windows 10 or Windows 11.
2. **Python**: Python 3.9, 3.10, 3.11, or 3.12.
3. **Web Browser**: Google Chrome / Microsoft Edge / Brave with an active **WhatsApp Web** session logged in.
4. **Display**: Recommended 1080p resolution or higher.

---

## 🚀 Installation & Setup

### 1. Clone the Repository
``bash
git clone https://github.com/your-username/whatsapp-automation-engine.git
cd whatsapp-automation-engine
``

### 2. Create and Activate Virtual Environment (Recommended)
``powershell
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1
``

### 3. Install Required Dependencies
``bash
pip install --upgrade pip
pip install -r requirements.txt
``

---

## 📋 Excel Contact Format

Your Excel file (contacts.xlsx or your custom .xlsx sheet) must include the following headers in the first row:

| name | mobile |
| :--- | :--- |
| Rajesh Sharma | 919876543210 |
| Priya Verma | 919123456789 |
| Amit Patel | 919988776655 |

> [!NOTE]
> - Ensure the mobile column includes the **Country Code** without + or spaces (e.g., 91 for India followed by the 10-digit number).
> - Make sure the column names 
ame and mobile are in lowercase.

---

## 🖥️ How to Use

1. **Login to WhatsApp Web**:
   - Open your browser and navigate to [https://web.whatsapp.com](https://web.whatsapp.com).
   - Ensure you are logged in and the browser window remains accessible.

2. **Run the Application**:
   ``powershell
   python whatsapp_ui.py
   ``

3. **Configure Campaign**:
   - Click **📂 SELECT CONTACTS** and choose your .xlsx file.
   - Edit your **Message Template** in the text editor. Use {name} where you want the recipient's name to appear:
     `	ext
     Namaste {name},

     This is a reminder that your quarterly tax compliance filing is scheduled.
     Please send the required documents.

     Regards,
     TaxOnline24.in Team
     `

4. **Launch Automation**:
   - Click **🚀 LAUNCH CAMPAIGN**.
   - Within the **10-second countdown**, switch your active window to the browser showing WhatsApp Web.
   - Keep the screen unobstructed while the automation engine processes messages safely.

5. **Campaign Completion**:
   - When finished, a summary alert will pop up.
   - An Excel report named Report_YYYYMMDD_HHMM.xlsx will be generated in the root directory.

---

## 📦 Building Standalone Executable (.exe)

You can compile this application into an independent Windows .exe using PyInstaller:

``powershell
pip install pyinstaller

pyinstaller --noconsole --onedir --add-data ""bg.png;."" --name ""WhatsAppEngine"" whatsapp_ui.py
``

The generated standalone application will be located inside the dist/WhatsAppEngine/ folder.

---

## ⚠️ Compliance & Disclaimer

> [!IMPORTANT]
> - This software is developed for legitimate client communication, compliance notifications, transactional updates, and educational automation purposes.
> - **Anti-Spam Notice**: Do NOT use this tool for unsolicited spam or bulk marketing. Sending unauthorized bulk messages violates WhatsApp's Terms of Service and can result in your phone number being banned.
> - The developer and contributors are **not responsible** for any misuse of this software, or for any account suspensions/bans imposed by WhatsApp LLC / Meta Platforms, Inc.

---

## 👨‍💻 Developer & Copyright

Developed with ❤️ by:

- **Author / Lead Developer:** Haresh Kumar Hemani
- **Website / Organization:** [TaxOnline24.in](https://www.taxonline24.in)
- **Official Website:** [https://www.taxonline24.in](https://www.taxonline24.in)
- **Official Inquiries & Email:** [contact@taxonline24.in](mailto:contact@taxonline24.in)

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE.md](LICENSE.md) file for complete copyright and legal terms.
