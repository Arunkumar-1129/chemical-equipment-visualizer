import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './History.css';

const History = ({ token, apiBaseUrl, onSelectDataset, onDownloadPDF }) => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadHistory = async () => {
      try {
        const response = await axios.get(
          `${apiBaseUrl}/history/`,
          { headers: { 'Authorization': `Token ${token}` } }
        );
        setHistory(response.data);
      } catch (err) {
        console.error('Failed to load history:', err);
      } finally {
        setLoading(false);
      }
    };

    loadHistory();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [apiBaseUrl, token]);

  if (loading) {
    return <div className="loading">Loading history...</div>;
  }

  if (history.length === 0) {
    return <div className="no-history">No upload history available</div>;
  }

  return (
    <div className="history-container">
      {history.map((item) => (
        <div key={item.id} className="history-item">
          <div className="history-info">
            <h4>{item.filename}</h4>
            <p className="history-date">
              Uploaded: {new Date(item.uploaded_at).toLocaleString()}
            </p>
            <p className="history-stats">
              Total Equipment: {item.total_count}
            </p>
          </div>
          <div className="history-actions">
            <button
              onClick={() => onSelectDataset(item.id)}
              className="btn btn-primary"
            >
              View
            </button>
            <button
              onClick={() => onDownloadPDF(item.id)}
              className="btn btn-secondary"
            >
              Download PDF
            </button>
          </div>
        </div>
      ))}
    </div>
  );
};

export default History;











