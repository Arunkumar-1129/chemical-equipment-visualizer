# Chemical Equipment Parameter Visualizer

A hybrid web + desktop application for visualizing and analyzing chemical equipment data from CSV files. Built with Django REST Framework backend, React.js web frontend, and PyQt5 desktop frontend.

## Features

- ✅ **CSV Upload**: Upload CSV files with equipment data (Web & Desktop)
- ✅ **Data Analysis**: Automatic calculation of summary statistics
- ✅ **Visualizations**: Interactive charts using Chart.js (Web) and Matplotlib (Desktop)
- ✅ **History Management**: Store and view last 5 uploaded datasets
- ✅ **PDF Reports**: Generate PDF reports for datasets
- ✅ **Authentication**: Basic token-based authentication
- ✅ **Data Tables**: View equipment data in tabular format

## Tech Stack

### Backend
- Django 4.2.7
- Django REST Framework
- Pandas (data processing)
- ReportLab (PDF generation)
- SQLite (database)

### Web Frontend
- React.js 18.2.0
- Chart.js 4.4.0
- Axios (HTTP client)

### Desktop Frontend
- PyQt5 5.15.10
- Matplotlib 3.8.2

## Project Structure

```
iitb/
├── backend/                 # Django backend
│   ├── config/             # Django settings
│   ├── equipment/          # Main app
│   │   ├── models.py       # Database models
│   │   ├── views.py        # API views
│   │   ├── serializers.py  # DRF serializers
│   │   └── urls.py         # URL routing
│   ├── manage.py
│   └── requirements.txt
├── frontend/               # React web app
│   ├── public/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
├── desktop/                # PyQt5 desktop app
│   ├── main.py
│   └── requirements.txt
├── sample_equipment_data.csv  # Sample data file
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 14+ and npm
- Git

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser (optional, for admin access):
```bash
python manage.py createsuperuser
```

6. Start the Django server:
```bash
python manage.py runserver
```

The backend API will be available at `http://localhost:8000/api/`

### Web Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The web app will open at `http://localhost:3000`

### Desktop Application Setup

1. Navigate to the desktop directory:
```bash
cd desktop
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Usage

### 1. Register/Login

- **Web**: Open `http://localhost:3000` and register a new account or login
- **Desktop**: Launch the app and register/login through the dialog

### 2. Upload CSV File

The CSV file must have the following columns:
- `Equipment Name`
- `Type`
- `Flowrate`
- `Pressure`
- `Temperature`

You can use the provided `sample_equipment_data.csv` for testing.

### 3. View Data

After uploading, you can:
- View summary statistics (total count, averages)
- See equipment type distribution
- View data in tabular format
- Explore interactive charts
- Access upload history (last 5 datasets)
- Download PDF reports

## API Endpoints

- `POST /api/register/` - Register new user
- `POST /api/login/` - Login user
- `POST /api/upload/` - Upload CSV file (requires authentication)
- `GET /api/summary/` - Get latest summary (requires authentication)
- `GET /api/summary/<id>/` - Get summary by dataset ID
- `GET /api/history/` - Get upload history (last 5)
- `GET /api/dataset/<id>/` - Get full dataset data
- `GET /api/dataset/<id>/pdf/` - Generate PDF report

## Sample Data Format

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Reactor-001,Reactor,150.5,2.5,85.3
Distillation-001,Distillation Column,200.0,1.8,120.5
```

## Development Notes

- The backend stores the last 5 datasets per user automatically
- All API endpoints require token authentication (except register/login)
- CORS is enabled for `http://localhost:3000`
- The database is SQLite (db.sqlite3) in the backend directory

## Troubleshooting

### Backend Issues
- Ensure Django server is running on port 8000
- Check that migrations are applied: `python manage.py migrate`
- Verify all dependencies are installed: `pip install -r requirements.txt`

### Frontend Issues
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Check that backend is running and accessible
- Verify CORS settings in Django settings.py

### Desktop App Issues
- Ensure PyQt5 is properly installed
- Check that backend API is accessible
- Verify matplotlib backend compatibility

## License

This project is created for IITB intern screening task.

## Author

Created as part of the IITB Intern Screening Task - Hybrid Web + Desktop Application











