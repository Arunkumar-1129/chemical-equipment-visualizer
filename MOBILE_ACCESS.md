# How to Access the App on Your Phone

## Step 1: Find Your Computer's IP Address

### Windows:
1. Open Command Prompt or PowerShell
2. Type: `ipconfig`
3. Look for **IPv4 Address** under your active network adapter (usually WiFi or Ethernet)
   - Example: `192.168.1.100` or `10.0.0.5`

### Mac/Linux:
1. Open Terminal
2. Type: `ifconfig` or `ip addr`
3. Look for your network interface (usually `en0` for WiFi or `eth0` for Ethernet)
   - Find the `inet` address (e.g., `192.168.1.100`)

## Step 2: Update React App to Use Your IP Address

### Option A: Quick Fix (Temporary)
1. Open `frontend/src/App.js`
2. Replace `http://localhost:8000/api` with `http://YOUR_IP_ADDRESS:8000/api`
   - Example: `http://192.168.1.100:8000/api`
3. Save the file
4. Restart the React dev server (`npm start`)

### Option B: Environment Variable (Recommended)
1. Create a file `frontend/.env` with:
   ```
   REACT_APP_API_URL=http://YOUR_IP_ADDRESS:8000/api
   ```
2. Update `frontend/src/App.js` to use:
   ```javascript
   const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';
   ```

## Step 3: Start Servers with Network Access

### Backend (Django):
```bash
cd backend
python manage.py runserver 0.0.0.0:8000
```
The `0.0.0.0` makes it accessible from any device on your network.

### Frontend (React):
```bash
cd frontend
set HOST=0.0.0.0 && npm start
```
Or on Mac/Linux:
```bash
cd frontend
HOST=0.0.0.0 npm start
```

## Step 4: Access from Your Phone

1. **Make sure your phone is on the same WiFi network** as your computer
2. Open your phone's browser
3. Go to: `http://YOUR_IP_ADDRESS:3000`
   - Example: `http://192.168.1.100:3000`

## Troubleshooting

### Can't connect from phone?
- ✅ Check that both devices are on the same WiFi network
- ✅ Disable Windows Firewall temporarily or allow ports 3000 and 8000
- ✅ Make sure you're using `0.0.0.0` when starting servers
- ✅ Verify the IP address is correct

### CORS errors?
- The backend is already configured to allow all origins
- If you still see CORS errors, restart the Django server

### Connection refused?
- Make sure both servers are running
- Check that your firewall isn't blocking the ports
- Try accessing `http://YOUR_IP:8000/api/` directly in phone browser to test backend

## Quick Setup Script

Create a file `start_mobile.bat` (Windows) or `start_mobile.sh` (Mac/Linux):

**Windows (`start_mobile.bat`):**
```batch
@echo off
echo Starting servers for mobile access...
echo.
echo Step 1: Find your IP address with: ipconfig
echo Step 2: Update frontend/src/App.js with your IP
echo.
echo Starting backend on 0.0.0.0:8000...
start cmd /k "cd backend && python manage.py runserver 0.0.0.0:8000"
timeout /t 3
echo Starting frontend on 0.0.0.0:3000...
start cmd /k "cd frontend && set HOST=0.0.0.0 && npm start"
echo.
echo Servers started! Access from phone at: http://YOUR_IP:3000
pause
```

**Mac/Linux (`start_mobile.sh`):**
```bash
#!/bin/bash
echo "Starting servers for mobile access..."
echo ""
echo "Step 1: Find your IP address with: ifconfig"
echo "Step 2: Update frontend/src/App.js with your IP"
echo ""
echo "Starting backend on 0.0.0.0:8000..."
cd backend && python manage.py runserver 0.0.0.0:8000 &
sleep 3
echo "Starting frontend on 0.0.0.0:3000..."
cd ../frontend && HOST=0.0.0.0 npm start
```










