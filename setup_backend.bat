@echo off
echo Setting up Django Backend...
cd backend
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
echo.
echo Backend setup complete!
echo To start the server, run: python manage.py runserver
pause











