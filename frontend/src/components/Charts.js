import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar, Pie, Line } from   'react-chartjs-2';
import './Charts.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const Charts = ({ data, summary }) => {
  // Equipment Type Distribution Chart
  const typeDistribution = summary.equipment_type_distribution || {};
  const typeChartData = {
    labels: Object.keys(typeDistribution),
    datasets: [
      {
        label: 'Count',
        data: Object.values(typeDistribution),
        backgroundColor: [
          'rgba(102, 126, 234, 0.8)',
          'rgba(118, 75, 162, 0.8)',
          'rgba(255, 99, 132, 0.8)',
          'rgba(54, 162, 235, 0.8)',
          'rgba(255, 206, 86, 0.8)',
          'rgba(75, 192, 192, 0.8)',
        ],
      },
    ],
  };

  // Flowrate vs Pressure Scatter/Line Chart
  const flowrateData = data.map(item => item.Flowrate || 0);
  const pressureData = data.map(item => item.Pressure || 0);
  const equipmentNames = data.map(item => item['Equipment Name'] || '');
  // const temperatureData = data.map(item => item.Temperature || 0); // Reserved for future use

  const parameterChartData = {
    labels: equipmentNames.slice(0, 20), // Limit to first 20 for readability
    datasets: [
      {
        label: 'Flowrate',
        data: flowrateData.slice(0, 20),
        borderColor: 'rgba(102, 126, 234, 1)',
        backgroundColor: 'rgba(102, 126, 234, 0.2)',
        yAxisID: 'y',
      },
      {
        label: 'Pressure',
        data: pressureData.slice(0, 20),
        borderColor: 'rgba(118, 75, 162, 1)',
        backgroundColor: 'rgba(118, 75, 162, 0.2)',
        yAxisID: 'y1',
      },
    ],
  };

  const parameterChartOptions = {
    responsive: true,
    interaction: {
      mode: 'index',
      intersect: false,
    },
    scales: {
      y: {
        type: 'linear',
        display: true,
        position: 'left',
        title: {
          display: true,
          text: 'Flowrate',
        },
      },
      y1: {
        type: 'linear',
        display: true,
        position: 'right',
        title: {
          display: true,
          text: 'Pressure',
        },
        grid: {
          drawOnChartArea: false,
        },
      },
    },
  };

  // Average Parameters Bar Chart
  const avgChartData = {
    labels: ['Flowrate', 'Pressure', 'Temperature'],
    datasets: [
      {
        label: 'Average Values',
        data: [
          summary.avg_flowrate || 0,
          summary.avg_pressure || 0,
          summary.avg_temperature || 0,
        ],
        backgroundColor: [
          'rgba(102, 126, 234, 0.8)',
          'rgba(118, 75, 162, 0.8)',
          'rgba(255, 99, 132, 0.8)',
        ],
      },
    ],
  };

  return (
    <div className="charts-container">
      <div className="chart-item">
        <h3>Equipment Type Distribution</h3>
        <div className="chart-wrapper">
          <Pie data={typeChartData} />
        </div>
      </div>

      <div className="chart-item">
        <h3>Average Parameters</h3>
        <div className="chart-wrapper">
          <Bar data={avgChartData} />
        </div>
      </div>

      <div className="chart-item full-width">
        <h3>Flowrate vs Pressure (First 20 Equipment)</h3>
        <div className="chart-wrapper">
          <Line data={parameterChartData} options={parameterChartOptions} />
        </div>
      </div>
    </div>
  );
};

export default Charts;











