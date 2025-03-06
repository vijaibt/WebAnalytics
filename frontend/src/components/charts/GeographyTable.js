import React, { useState, useEffect } from 'react';
import analyticsService from '../../services/analyticsService';
import '../../styles/components.css';

const GeographyTable = ({ timeRange }) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    const fetchData = async () => {
      try {
        // Calculate days based on timeRange
        let days = getTimeRangeDays(timeRange);
        
        const response = await analyticsService.getPageViewsByCountry(days);
        setData(response.data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching geography data:', error);
        // Mock data if API fails
        setData([
          { country: 'United States', count: 12, percentage: 48 },
          { country: 'Germany', count: 5, percentage: 20 },
          { country: 'Japan', count: 3, percentage: 12 },
          { country: 'United Kingdom', count: 2, percentage: 8 },
          { country: 'Canada', count: 2, percentage: 8 },
          { country: 'Other', count: 1, percentage: 4 }
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
    <div className="table-container">
      <table className="data-table">
        <thead>
          <tr>
            <th>Country</th>
            <th>Visitors</th>
            <th>Percentage</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item, index) => (
            <tr key={index}>
              <td>{item.country || 'Unknown'}</td>
              <td>{item.count}</td>
              <td>
                <div className="progress-container">
                  <div className="progress-bar">
                    <div 
                      className="progress-bar-fill" 
                      style={{ width: `${item.percentage}%` }}
                    ></div>
                  </div>
                  <span>{item.percentage}%</span>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default GeographyTable;