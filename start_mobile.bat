@echo off
echo ========================================
echo Mobile Access Setup
echo ========================================
echo.
echo Step 1: Finding your IP address...
ipconfig | findstr /i "IPv4"
echo.
echo Copy the IPv4 address above (e.g., 192.168.1.100)
echo.
pause
echo.
echo Step 2: Starting servers for mobile access...
echo.
echo Starting Django backend on 0.0.0.0:8000...
start "Django Backend" cmd /k "cd backend && venv\Scripts\activate && python manage.py runserver 0.0.0.0:8000"
timeout /t 3
echo.
echo Starting React frontend on 0.0.0.0:3000...
start "React Frontend" cmd /k "cd frontend && set HOST=0.0.0.0 && npm start"
echo.
echo ========================================
echo Servers are starting!
echo ========================================
echo.
echo IMPORTANT: Before accessing from phone:
echo 1. Create file: frontend\.env
echo 2. Add this line: REACT_APP_API_URL=http://YOUR_IP:8000/api
echo    (Replace YOUR_IP with the IP address from above)
echo 3. Restart the React server
echo.
echo Then access from your phone at: http://YOUR_IP:3000
echo.
pause










