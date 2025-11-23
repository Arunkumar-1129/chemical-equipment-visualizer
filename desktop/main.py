import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFileDialog, 
                             QTableWidget, QTableWidgetItem, QMessageBox,
                             QTabWidget, QGroupBox, QGridLayout, QTextEdit, QLineEdit)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
import requests
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


class APIWorker(QThread):
    """Worker thread for API calls"""
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, method, url, headers=None, data=None, files=None):
        super().__init__()
        self.method = method
        self.url = url
        self.headers = headers or {}
        self.data = data
        self.files = files

    def run(self):
        try:
            if self.method == 'GET':
                response = requests.get(self.url, headers=self.headers)
            elif self.method == 'POST':
                if self.files:
                    response = requests.post(self.url, headers=self.headers, 
                                            files=self.files, data=self.data)
                else:
                    response = requests.post(self.url, headers=self.headers, 
                                           json=self.data)
            
            response.raise_for_status()
            if response.headers.get('content-type', '').startswith('application/json'):
                self.finished.emit(response.json())
            else:
                self.finished.emit({'success': True, 'data': response.content})
        except Exception as e:
            self.error.emit(str(e))


class LoginDialog(QWidget):
    """Login/Register Dialog"""
    login_success = pyqtSignal(str, dict)

    def __init__(self, api_base_url):
        super().__init__()
        self.api_base_url = api_base_url
        self.token = None
        self.user = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Chemical Equipment Visualizer - Login')
        self.setGeometry(300, 300, 400, 300)
        
        layout = QVBoxLayout()
        
        self.title = QLabel('Chemical Equipment Visualizer')
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont('Arial', 16, QFont.Bold))
        layout.addWidget(self.title)
        
        self.subtitle = QLabel('Sign in to continue')
        self.subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.subtitle)
        
        self.username_label = QLabel('Username:')
        layout.addWidget(self.username_label)
        self.username_input = QLineEdit()
        layout.addWidget(self.username_input)
        
        self.password_label = QLabel('Password:')
        layout.addWidget(self.password_label)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText('Password')
        layout.addWidget(self.password_input)
        
        self.email_label = QLabel('Email (for registration):')
        layout.addWidget(self.email_label)
        self.email_input = QLineEdit()
        layout.addWidget(self.email_input)
        
        button_layout = QHBoxLayout()
        self.login_btn = QPushButton('Login')
        self.login_btn.clicked.connect(self.login)
        self.register_btn = QPushButton('Register')
        self.register_btn.clicked.connect(self.register)
        button_layout.addWidget(self.login_btn)
        button_layout.addWidget(self.register_btn)
        layout.addLayout(button_layout)
        
        self.status_label = QLabel('')
        self.status_label.setStyleSheet('color: red;')
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)

    def get_username(self):
        return self.username_input.text().strip()

    def get_password(self):
        return self.password_input.text().strip()

    def get_email(self):
        return self.email_input.text().strip()

    def login(self):
        username = self.get_username()
        password = self.get_password()
        
        if not username or not password:
            self.status_label.setText('Please enter username and password')
            return
        
        self.worker = APIWorker('POST', f'{self.api_base_url}/login/', 
                               data={'username': username, 'password': password})
        self.worker.finished.connect(self.on_login_success)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def register(self):
        username = self.get_username()
        password = self.get_password()
        email = self.get_email()
        
        if not username or not password:
            self.status_label.setText('Please enter username and password')
            return
        
        self.worker = APIWorker('POST', f'{self.api_base_url}/register/', 
                               data={'username': username, 'password': password, 
                                    'email': email})
        self.worker.finished.connect(self.on_register_success)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_login_success(self, response):
        if 'token' in response:
            self.token = response['token']
            self.user = {'id': response['user_id'], 'username': response['username']}
            self.login_success.emit(self.token, self.user)
        else:
            self.status_label.setText('Login failed')

    def on_register_success(self, response):
        if 'token' in response:
            self.token = response['token']
            self.user = {'id': response['user_id'], 'username': response['username']}
            self.login_success.emit(self.token, self.user)
        else:
            self.status_label.setText('Registration failed')

    def on_error(self, error_msg):
        self.status_label.setText(f'Error: {error_msg}')


class ChartWidget(QWidget):
    """Widget for displaying matplotlib charts"""
    def __init__(self):
        super().__init__()
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def plot_pie(self, labels, values, title):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.set_title(title)
        self.canvas.draw()

    def plot_bar(self, labels, values, title, ylabel):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.bar(labels, values, color=['#667eea', '#764ba2', '#ff6384'])
        ax.set_title(title)
        ax.set_ylabel(ylabel)
        self.canvas.draw()

    def plot_line(self, x_data, y_data, labels, title):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        for i, (y, label) in enumerate(zip(y_data, labels)):
            ax.plot(x_data[:20], y[:20], marker='o', label=label)
        ax.set_title(title)
        ax.set_xlabel('Equipment Index')
        ax.legend()
        ax.grid(True)
        self.canvas.draw()


class MainWindow(QMainWindow):
    """Main application window"""
    def __init__(self):
        super().__init__()
        self.api_base_url = 'http://localhost:8000/api'
        self.token = None
        self.user = None
        self.current_data = None
        self.current_summary = None
        self.init_ui()
        self.show_login()

    def init_ui(self):
        self.setWindowTitle('Chemical Equipment Parameter Visualizer')
        self.setGeometry(100, 100, 1200, 800)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout()
        central_widget.setLayout(self.main_layout)

    def show_login(self):
        """Show login dialog"""
        self.login_dialog = LoginDialog(self.api_base_url)
        self.login_dialog.login_success.connect(self.on_login_success)
        self.login_dialog.show()

    def on_login_success(self, token, user):
        self.token = token
        self.user = user
        self.login_dialog.close()
        self.setup_dashboard()

    def setup_dashboard(self):
        """Setup main dashboard"""
        # Clear existing widgets
        for i in reversed(range(self.main_layout.count())):
            self.main_layout.itemAt(i).widget().setParent(None)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel('Chemical Equipment Parameter Visualizer')
        title.setFont(QFont('Arial', 18, QFont.Bold))
        header_layout.addWidget(title)
        header_layout.addStretch()
        user_label = QLabel(f'Welcome, {self.user["username"]}!')
        header_layout.addWidget(user_label)
        logout_btn = QPushButton('Logout')
        logout_btn.clicked.connect(self.logout)
        header_layout.addWidget(logout_btn)
        self.main_layout.addLayout(header_layout)
        
        # Tabs
        tabs = QTabWidget()
        
        # Upload Tab
        upload_tab = QWidget()
        upload_layout = QVBoxLayout()
        upload_btn = QPushButton('Upload CSV File')
        upload_btn.clicked.connect(self.upload_file)
        upload_btn.setStyleSheet('font-size: 14px; padding: 10px;')
        upload_layout.addWidget(upload_btn)
        self.status_label = QLabel('')
        upload_layout.addWidget(self.status_label)
        upload_tab.setLayout(upload_layout)
        tabs.addTab(upload_tab, 'Upload')
        
        # Summary Tab
        self.summary_tab = QWidget()
        self.summary_layout = QVBoxLayout()
        self.summary_tab.setLayout(self.summary_layout)
        tabs.addTab(self.summary_tab, 'Summary')
        
        # Data Table Tab
        self.table_tab = QWidget()
        self.table_layout = QVBoxLayout()
        self.data_table = QTableWidget()
        self.table_layout.addWidget(self.data_table)
        self.table_tab.setLayout(self.table_layout)
        tabs.addTab(self.table_tab, 'Data Table')
        
        # Charts Tab
        self.charts_tab = QWidget()
        self.charts_layout = QVBoxLayout()
        self.charts_tab.setLayout(self.charts_layout)
        tabs.addTab(self.charts_tab, 'Charts')
        
        # History Tab
        self.history_tab = QWidget()
        self.history_layout = QVBoxLayout()
        refresh_btn = QPushButton('Refresh History')
        refresh_btn.clicked.connect(self.load_history)
        self.history_layout.addWidget(refresh_btn)
        self.history_list = QTextEdit()
        self.history_list.setReadOnly(True)
        self.history_layout.addWidget(self.history_list)
        self.history_tab.setLayout(self.history_layout)
        tabs.addTab(self.history_tab, 'History')
        
        self.main_layout.addWidget(tabs)
        
        # Load latest data
        self.load_latest_data()
        self.load_history()

    def upload_file(self):
        """Handle file upload"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Select CSV File', '', 'CSV Files (*.csv)'
        )
        
        if not file_path:
            return
        
        self.status_label.setText('Uploading...')
        
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f, 'text/csv')}
            self.worker = APIWorker(
                'POST',
                f'{self.api_base_url}/upload/',
                headers={'Authorization': f'Token {self.token}'},
                files=files
            )
            self.worker.finished.connect(self.on_upload_success)
            self.worker.error.connect(self.on_upload_error)
            self.worker.start()

    def on_upload_success(self, response):
        self.status_label.setText('Upload successful!')
        self.current_data = response.get('data', [])
        self.current_summary = response.get('summary', {})
        self.update_display()
        self.load_history()

    def on_upload_error(self, error_msg):
        self.status_label.setText(f'Upload failed: {error_msg}')
        QMessageBox.critical(self, 'Error', f'Upload failed: {error_msg}')

    def load_latest_data(self):
        """Load latest dataset"""
        self.worker = APIWorker(
            'GET',
            f'{self.api_base_url}/summary/',
            headers={'Authorization': f'Token {self.token}'}
        )
        self.worker.finished.connect(self.on_load_data_success)
        self.worker.error.connect(lambda e: None)  # Silent fail if no data
        self.worker.start()

    def on_load_data_success(self, response):
        if 'summary' in response:
            dataset_id = response.get('id')
            self.current_summary = response.get('summary', {})
            
            # Load full data
            self.worker = APIWorker(
                'GET',
                f'{self.api_base_url}/dataset/{dataset_id}/',
                headers={'Authorization': f'Token {self.token}'}
            )
            self.worker.finished.connect(self.on_load_full_data)
            self.worker.start()

    def on_load_full_data(self, response):
        self.current_data = response.get('raw_data', [])
        self.update_display()

    def update_display(self):
        """Update all displays with current data"""
        if self.current_summary:
            self.update_summary()
        if self.current_data:
            self.update_table()
            self.update_charts()

    def update_summary(self):
        """Update summary tab"""
        for i in reversed(range(self.summary_layout.count())):
            self.summary_layout.itemAt(i).widget().setParent(None)
        
        summary_group = QGroupBox('Summary Statistics')
        summary_grid = QGridLayout()
        
        summary_grid.addWidget(QLabel('Total Equipment:'), 0, 0)
        summary_grid.addWidget(QLabel(str(self.current_summary.get('total_count', 0))), 0, 1)
        
        summary_grid.addWidget(QLabel('Avg Flowrate:'), 1, 0)
        avg_flow = self.current_summary.get('avg_flowrate', 0)
        summary_grid.addWidget(QLabel(f'{avg_flow:.2f}' if avg_flow else 'N/A'), 1, 1)
        
        summary_grid.addWidget(QLabel('Avg Pressure:'), 2, 0)
        avg_press = self.current_summary.get('avg_pressure', 0)
        summary_grid.addWidget(QLabel(f'{avg_press:.2f}' if avg_press else 'N/A'), 2, 1)
        
        summary_grid.addWidget(QLabel('Avg Temperature:'), 3, 0)
        avg_temp = self.current_summary.get('avg_temperature', 0)
        summary_grid.addWidget(QLabel(f'{avg_temp:.2f}' if avg_temp else 'N/A'), 3, 1)
        
        summary_group.setLayout(summary_grid)
        self.summary_layout.addWidget(summary_group)
        
        # Equipment type distribution
        dist = self.current_summary.get('equipment_type_distribution', {})
        if dist:
            dist_group = QGroupBox('Equipment Type Distribution')
            dist_layout = QVBoxLayout()
            dist_text = QTextEdit()
            dist_text.setReadOnly(True)
            dist_text.setMaximumHeight(200)
            dist_text.setText('\n'.join([f'{k}: {v}' for k, v in dist.items()]))
            dist_layout.addWidget(dist_text)
            dist_group.setLayout(dist_layout)
            self.summary_layout.addWidget(dist_group)
        
        self.summary_layout.addStretch()

    def update_table(self):
        """Update data table"""
        if not self.current_data:
            return
        
        self.data_table.setRowCount(len(self.current_data))
        if self.current_data:
            columns = list(self.current_data[0].keys())
            self.data_table.setColumnCount(len(columns))
            self.data_table.setHorizontalHeaderLabels(columns)
            
            for row_idx, row_data in enumerate(self.current_data):
                for col_idx, col_name in enumerate(columns):
                    value = row_data.get(col_name, '')
                    if isinstance(value, (int, float)):
                        value = f'{value:.2f}'
                    self.data_table.setItem(row_idx, col_idx, 
                                          QTableWidgetItem(str(value)))

    def update_charts(self):
        """Update charts"""
        for i in reversed(range(self.charts_layout.count())):
            self.charts_layout.itemAt(i).widget().setParent(None)
        
        if not self.current_data or not self.current_summary:
            return
        
        # Pie chart for equipment type distribution
        dist = self.current_summary.get('equipment_type_distribution', {})
        if dist:
            pie_chart = ChartWidget()
            pie_chart.plot_pie(
                list(dist.keys()),
                list(dist.values()),
                'Equipment Type Distribution'
            )
            self.charts_layout.addWidget(pie_chart)
        
        # Bar chart for averages
        avg_chart = ChartWidget()
        avg_chart.plot_bar(
            ['Flowrate', 'Pressure', 'Temperature'],
            [
                self.current_summary.get('avg_flowrate', 0) or 0,
                self.current_summary.get('avg_pressure', 0) or 0,
                self.current_summary.get('avg_temperature', 0) or 0
            ],
            'Average Parameters',
            'Value'
        )
        self.charts_layout.addWidget(avg_chart)
        
        # Line chart for flowrate and pressure
        if self.current_data:
            flowrate_data = [item.get('Flowrate', 0) or 0 for item in self.current_data]
            pressure_data = [item.get('Pressure', 0) or 0 for item in self.current_data]
            indices = list(range(len(self.current_data)))
            
            line_chart = ChartWidget()
            line_chart.plot_line(
                indices,
                [flowrate_data[:20], pressure_data[:20]],
                ['Flowrate', 'Pressure'],
                'Flowrate vs Pressure (First 20 Equipment)'
            )
            self.charts_layout.addWidget(line_chart)
        
        self.charts_layout.addStretch()

    def load_history(self):
        """Load upload history"""
        self.worker = APIWorker(
            'GET',
            f'{self.api_base_url}/history/',
            headers={'Authorization': f'Token {self.token}'}
        )
        self.worker.finished.connect(self.on_history_loaded)
        self.worker.error.connect(lambda e: self.history_list.setText('Failed to load history'))
        self.worker.start()

    def on_history_loaded(self, response):
        if isinstance(response, list):
            history_text = 'Upload History (Last 5):\n\n'
            for item in response:
                history_text += f"File: {item.get('filename', 'N/A')}\n"
                history_text += f"Uploaded: {item.get('uploaded_at', 'N/A')}\n"
                history_text += f"Total Equipment: {item.get('total_count', 0)}\n"
                history_text += f"ID: {item.get('id', 'N/A')}\n"
                history_text += '-' * 40 + '\n'
            self.history_list.setText(history_text)

    def logout(self):
        """Logout and return to login"""
        self.token = None
        self.user = None
        self.current_data = None
        self.current_summary = None
        for i in reversed(range(self.main_layout.count())):
            self.main_layout.itemAt(i).widget().setParent(None)
        self.show_login()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

