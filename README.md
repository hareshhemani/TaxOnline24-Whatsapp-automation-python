# 🚀 Enterprise WhatsApp Automation Engine - Version 2.0
### Advanced Client Communication Suite with Image & Document Attachments

---

## 🌟 What's New in Version 2.0?

1. 📎 **Media & Document Attachments Support**:
   - Send **Images** (`.png`, `.jpg`, `.jpeg`, `.bmp`, `.webp`).
   - Send **Documents & Files** (`.pdf`, `.docx`, `.xlsx`, `.txt`, `.csv`, `.zip`).
   - Native Windows Clipboard integration (`CF_HDROP` & `CF_DIB`) for seamless WhatsApp Web upload.

2. 🔀 **Dual Attachment Modes**:
   - **Mode A (Common File)**: Select an attachment from the GUI using `📎 ATTACH IMAGE / DOC` to send the same flyer/document to all contacts.
   - **Mode B (Per-Client Attachment via Excel)**: If your Excel file has an `attachment` column containing individual file paths (e.g., `C:\Invoices\101.pdf`), the engine will automatically send each client's personalized attachment!

3. 💬 **Dynamic Caption Handling**:
   - When an attachment is selected, the message template automatically becomes the **caption** of the media/document, still supporting the `{name}` placeholder!
   - If no attachment is selected, it seamlessly runs in **Text-Only Mode**.

4. 📊 **Enhanced Audit Trail**:
   - Reports (`Report_v2_YYYYMMDD_HHMM.xlsx`) track both delivery status and the exact attachment sent (`Attachment_Sent` column).

---

## 📋 Excel Format

Your Excel file (`.xlsx` or `.xls`) must contain at least:
| name | mobile | attachment (Optional) |
|---|---|---|
| Ramesh Sharma | 919876543210 | C:\Bills\Ramesh_Bill.pdf |
| Sunita Verma | 919812345678 | C:\Bills\Sunita_Bill.pdf |

*(Note: If `attachment` column is omitted, the common file selected from the GUI will be used).*

---

## 🚀 How to Run Version 2.0

```powershell
# Navigate to Version 2.0
cd "Version 2.0"

# Run the application
python whatsapp_ui.py
```
