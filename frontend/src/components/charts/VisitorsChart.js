// In src/components/charts/VisitorsChart.js
import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import analyticsService from '../../services/analyticsService';
import '../../styles/components.css';

const VisitorsChart = ({ timeRange }) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    // Calculate days based on timeRange
    let days = 30;
    switch (timeRange) {
      case 'Today':
        days = 1;
        break;
      case 'Yesterday':
        days = 2;
        break;
      case '7D':
        days = 7;
        break;
      case '30D':
        days = 30;
        break;
      case '3M':
        days = 90;
        break;
      default:
        days = 30;
    }
    
    const fetchData = async () => {
      try {
        const response = await analyticsService.getDailyActiveUsers(days);
        
        // Format the data for the chart
        const formattedData = response.data.map(item => ({
          date: new Date(item.day).toLocaleDateString(),
          value: item.count
        }));
        
        setData(formattedData);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching visitor data:', error);
        setLoading(false);
      }
    };
    
    fetchData();
  }, [timeRange]);
  
  if (loading) {
    return <div className="loading">Loading...</div>;
  }
  
  return (
    <div className="chart-container">
      <h3>Daily Active Users</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="value" stroke="#8884d8" name="Active Users" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default VisitorsChart;