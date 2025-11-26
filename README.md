# 🤖 BotCity OrangeHRM Automation Challenge

Automates adding candidates to OrangeHRM from a CSV file.  
Generates a TXT resume for each candidate, uploads it, and saves the record.

---

## ✨ Features
- ✅ Login to OrangeHRM
- ✅ Read candidates from CSV
- ✅ Fill personal and job info
- ✅ Generate and upload resumes
- ✅ Save candidate records
- 🔁 Retry mechanism for temporary failures

---

## ⚙️ Requirements
- Python 3.11+
- Selenium WebDriver
- Dependencies: `selenium`, `requests`, `retry`, `pathlib`

---

## 🚀 Usage
Run the main bot script:

```bash
python bot.py
CSV is downloaded automatically.

Output files and resumes are saved in output/.

🗂 File Structure
bot.py                  # Main script
resources/              # Helper modules and locators
output/                 # Generated resumes and downloaded CSV
