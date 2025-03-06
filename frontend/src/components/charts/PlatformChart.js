import React, { useState, useEffect } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import analyticsService from '../../services/analyticsService';
import '../../styles/components.css';

const PlatformChart = ({ timeRange }) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  
  const COLORS = ['#8884d8', '#83a6ed', '#8dd1e1', '#82ca9d', '#a4de6c', '#d0ed57'];
  
  useEffect(() => {
    const fetchData = async () => {
      try {
        // Calculate days based on timeRange
        let days = getTimeRangeDays(timeRange);
        
        const response = await analyticsService.getPlatformData(days);
        setData(response.data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching platform data:', error);
        // Mock data if API fails
        setData([
          { name: 'Desktop', value: 45 },
          { name: 'Mobile', value: 35 },
          { name: 'Tablet', value: 20 }
        ]);
        setLoading(false);
      }
    };
    
    fetchData();
  }, [timeRange]);
  
  const getTimeRangeDays = (range) => {
    switch (range) {
      case 'Today': return 1;
      case 'Yesterday': return 2;
      case '7D': return 7;
      case '30D': return 30;
      case '3M': return 90;
      default: return 7;
    }
  };
  
  if (loading) {
    return <div className="loading">Loading...</div>;
  }
  
  return (
    <div className="chart-container" style={{ height: 300 }}>
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            labelLine={false}
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
            label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip formatter={(value) => `${value}`} />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};

export default PlatformChart;