import React from 'react';
import './DataTable.css';

const DataTable = ({ data }) => {
  if (!data || data.length === 0) {
    return <div className="no-data">No data available</div>;
  }

  const columns = Object.keys(data[0]);

  return (
    <div className="table-container">
      <table>
        <thead>
          <tr>
            {columns.map((col) => (
              <th key={col}>{col}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, idx) => (
            <tr key={idx}>
              {columns.map((col) => (
                <td key={col}>
                  {typeof row[col] === 'number' 
                    ? row[col].toFixed(2) 
                    : row[col]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default DataTable;











