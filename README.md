# 🏦 AI Disaster Claims Evaluator

## 📌 Overview
A FastAPI-based service that **automates insurance claim evaluation** for disaster-related events.  
It allows:
- Uploading and parsing policy documents (`PDF` / `DOCX`)
- Processing claim text using AI to return **approval likelihood** and **confidence scores**

Built for **HackRx Qualifier 2025** 🚀

---

## ⚡ Quick Start (Windows PowerShell)
```powershell
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
.\venv\Scripts\Activate.ps1
# If blocked, run:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 3. Upgrade pip
pip install --upgrade pip

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run FastAPI server
uvicorn main:app --reload
Open: http://127.0.0.1:8000/docs to test the API (Swagger UI).

