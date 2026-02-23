import React, { useState, useEffect } from 'react';
import axios from 'axios';
import DataTable from './DataTable';
import Charts from './Charts';
import History from './History';
import './Dashboard.css';

const Dashboard = ({ token, user, onLogout, apiBaseUrl }) => {
  const [currentData, setCurrentData] = useState(null);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const axiosConfig = {
    headers: {
      'Authorization': `Token ${token}`,
      'Content-Type': 'multipart/form-data'
    }
  };

  const handleFileUpload = async (file) => {
    setLoading(true);
    setError('');
    setSuccess('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(
        `${apiBaseUrl}/upload/`,
        formData,
        axiosConfig
      );
      
      setCurrentData(response.data.data);
      setSummary(response.data.summary);
      setSuccess('File uploaded successfully!');
    } catch (err) {
      setError(err.response?.data?.error || 'Upload failed');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const loadLatestData = async () => {
      try {
        const response = await axios.get(
          `${apiBaseUrl}/summary/`,
          { headers: { 'Authorization': `Token ${token}` } }
        );

        if (response.data.summary) {
          setSummary(response.data.summary);
          // Load full data
          const dataResponse = await axios.get(
            `${apiBaseUrl}/dataset/${response.data.id}/`,
            { headers: { 'Authorization': `Token ${token}` } }
          );
          setCurrentData(dataResponse.data.raw_data);
        }
      } catch (err) {
        // No data yet, that's okay
      }
    };

    loadLatestData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [apiBaseUrl, token]);

  const handleDownloadPDF = async (datasetId) => {
    try {
      const response = await axios.get(
        `${apiBaseUrl}/dataset/${datasetId}/pdf/`,
        {
          headers: { 'Authorization': `Token ${token}` },
          responseType: 'blob'
        }
      );
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `report_${datasetId}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      setError('Failed to generate PDF');
    }
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div className="header-content">
          <h1>Chemical Equipment Parameter Visualizer</h1>
          <div className="header-actions">
            <span className="user-info">Welcome, {user?.username}!</span>
            <button onClick={onLogout} className="btn btn-danger">Logout</button>
          </div>
        </div>
      </header>

      <div className="container">
        {error && <div className="error">{error}</div>}
        {success && <div className="success">{success}</div>}

        <div className="card">
          <h2>Upload CSV File</h2>
          <FileUpload 
            onUpload={handleFileUpload} 
            loading={loading}
          />
          <p className="help-text">
            Upload a CSV file with columns: Equipment Name, Type, Flowrate, Pressure, Temperature
          </p>
        </div>

        {summary && (
          <>
            <div className="card">
              <h2>Summary Statistics</h2>
              <SummaryDisplay summary={summary} />
            </div>

            <div className="card">
              <h2>Data Visualization</h2>
              {currentData && summary && (
                <Charts data={currentData} summary={summary} />
              )}
            </div>

            <div className="card">
              <h2>Equipment Data Table</h2>
              {currentData && (
                <DataTable data={currentData} />
              )}
            </div>
          </>
        )}

        <div className="card">
          <h2>Upload History</h2>
          <History 
            token={token}
            apiBaseUrl={apiBaseUrl}
            onSelectDataset={(datasetId) => {
              axios.get(
                `${apiBaseUrl}/dataset/${datasetId}/`,
                { headers: { 'Authorization': `Token ${token}` } }
              ).then(response => {
                setCurrentData(response.data.raw_data);
                setSummary({
                  total_count: response.data.total_count,
                  avg_flowrate: response.data.avg_flowrate,
                  avg_pressure: response.data.avg_pressure,
                  avg_temperature: response.data.avg_temperature,
                  equipment_type_distribution: response.data.equipment_type_distribution
                });
              });
            }}
            onDownloadPDF={handleDownloadPDF}
          />
        </div>
      </div>
    </div>
  );
};

const FileUpload = ({ onUpload, loading }) => {
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      onUpload(file);
    }
  };

  return (
    <div className="file-upload">
      <input
        type="file"
        accept=".csv"
        onChange={handleFileChange}
        disabled={loading}
        id="file-input"
        style={{ display: 'none' }}
      />
      <label htmlFor="file-input" className="file-upload-label">
        {loading ? 'Uploading...' : 'Choose CSV File'}
      </label>
    </div>
  );
};

const SummaryDisplay = ({ summary }) => {
  return (
    <div className="summary-grid">
      <div className="summary-item">
        <div className="summary-label">Total Equipment</div>
        <div className="summary-value">{summary.total_count}</div>
      </div>
      <div className="summary-item">
        <div className="summary-label">Avg Flowrate</div>
        <div className="summary-value">
          {summary.avg_flowrate ? summary.avg_flowrate.toFixed(2) : 'N/A'}
        </div>
      </div>
      <div className="summary-item">
        <div className="summary-label">Avg Pressure</div>
        <div className="summary-value">
          {summary.avg_pressure ? summary.avg_pressure.toFixed(2) : 'N/A'}
        </div>
      </div>
      <div className="summary-item">
        <div className="summary-label">Avg Temperature</div>
        <div className="summary-value">
          {summary.avg_temperature ? summary.avg_temperature.toFixed(2) : 'N/A'}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;











