# Quick Start Guide - How to Run the Application

## Prerequisites
- Python 3.8 or higher
- Node.js 14+ and npm
- Git (optional)

---

## Step 1: Setup and Run Backend (Django)

### Option A: Using Setup Script (Windows)
1. Double-click `setup_backend.bat`
2. Wait for installation to complete
3. The script will create a virtual environment and install dependencies

### Option B: Manual Setup
1. Open terminal/command prompt
2. Navigate to backend folder:
   ```bash
   cd backend
   ```
3. Create virtual environment:
   ```bash
   python -m venv venv
   ```
4. Activate virtual environment:
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **Linux/Mac:**
     ```bash
     source venv/bin/activate
     ```
5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
6. Run database migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
7. Start the Django server:
   ```bash
   python manage.py runserver
   ```

✅ **Backend is now running at:** `http://localhost:8000`

**Keep this terminal window open!**

---

## Step 2: Setup and Run Web Frontend (React)

### Option A: Using Setup Script (Windows)
1. Open a **NEW** terminal/command prompt window
2. Double-click `setup_frontend.bat` OR manually run:
   ```bash
   cd frontend
   npm install
   ```

### Option B: Manual Setup
1. Open a **NEW** terminal/command prompt window
2. Navigate to frontend folder:
   ```bash
   cd frontend
   ```
3. Install dependencies:
   ```bash
   npm install
   ```
   (This may take a few minutes on first run)

4. Start the React development server:
   ```bash
   npm start
   ```

✅ **Web app will automatically open at:** `http://localhost:3000`

**Keep this terminal window open!**

---

## Step 3: Run Desktop Application (PyQt5)

### Option A: Using Setup Script (Windows)
1. Open a **NEW** terminal/command prompt window
2. Double-click `setup_desktop.bat` OR manually run:
   ```bash
   cd desktop
   pip install -r requirements.txt
   ```

### Option B: Manual Setup
1. Open a **NEW** terminal/command prompt window
2. Navigate to desktop folder:
   ```bash
   cd desktop
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the desktop application:
   ```bash
   python main.py
   ```

✅ **Desktop app window will open!**

**Note:** Make sure the backend is running (Step 1) before starting the desktop app.

---

## Complete Setup Summary

You need **3 terminal windows** running simultaneously:

1. **Terminal 1:** Backend (Django) - `http://localhost:8000`
2. **Terminal 2:** Web Frontend (React) - `http://localhost:3000`
3. **Terminal 3:** Desktop App (PyQt5) - GUI window

---

## How to Use the Application

### First Time Setup:
1. **Register a new account:**
   - In web app: Click "Register" and create an account
   - In desktop app: Click "Register" button in login dialog

2. **Login:**
   - Use your username and password to login

### Upload CSV File:
1. Click "Upload CSV File" or "Choose CSV File"
2. Select `sample_equipment_data.csv` (in the root folder)
3. Wait for upload to complete

### View Results:
- **Summary Statistics:** Total count, averages
- **Charts:** Equipment type distribution, parameter comparisons
- **Data Table:** Full equipment data
- **History:** View last 5 uploaded files
- **PDF Report:** Download PDF report for any dataset

---

## Troubleshooting

### Backend Issues:
- **Port 8000 already in use:**
  ```bash
  python manage.py runserver 8001
  ```
  Then update `API_BASE_URL` in frontend/src/App.js and desktop/main.py

- **Module not found errors:**
  ```bash
  pip install -r requirements.txt
  ```

- **Database errors:**
  ```bash
  python manage.py migrate
  ```

### Frontend Issues:
- **Port 3000 already in use:**
  - React will ask to use a different port automatically

- **npm install fails:**
  ```bash
  npm cache clean --force
  npm install
  ```

- **CORS errors:**
  - Make sure backend is running
  - Check that CORS settings in `backend/config/settings.py` include `http://localhost:3000`

### Desktop App Issues:
- **PyQt5 installation fails:**
  ```bash
  pip install --upgrade pip
  pip install PyQt5
  ```

- **"Connection refused" errors:**
  - Make sure backend is running on `http://localhost:8000`

---

## Testing the Application

1. **Test with sample data:**
   - Use `sample_equipment_data.csv` provided in the root folder
   - Upload it through either web or desktop interface

2. **Verify features:**
   - ✅ CSV upload works
   - ✅ Summary statistics display correctly
   - ✅ Charts render properly
   - ✅ Data table shows all equipment
   - ✅ History shows uploaded files
   - ✅ PDF download works

---

## Stopping the Application

1. **Stop Backend:** Press `Ctrl+C` in Terminal 1
2. **Stop Web Frontend:** Press `Ctrl+C` in Terminal 2
3. **Stop Desktop App:** Close the window or press `Ctrl+C` in Terminal 3

---

## Need Help?

- Check the main `README.md` for detailed documentation
- Verify all prerequisites are installed
- Make sure all three services are running simultaneously
- Check terminal output for error messages











