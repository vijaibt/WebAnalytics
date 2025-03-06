// src/components/tables/PagesPerformanceTable.js
import React, { useState, useEffect } from 'react';
import analyticsService from '../../services/analyticsService';
import '../../styles/components.css';

const PagesPerformanceTable = ({ timeRange }) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    const fetchData = async () => {
      try {
        const days = getTimeRangeDays(timeRange);
        
        const response = await analyticsService.getTopPages(days);
        setData(response.data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching page performance data:', error);
        // Mock data if API fails
        setData([
          { 
            page: 'Home Page', 
            views: 760, 
            landing_page: 6335, 
            exit_page: 6560, 
            bounce_rate: 81.11 
          },
          { 
            page: 'Shop Page', 
            views: 687, 
            landing_page: 6007, 
            exit_page: 6236, 
            bounce_rate: 81.02 
          },
          { 
            page: 'FAQ Page', 
            views: 682, 
            landing_page: 529, 
            exit_page: 518, 
            bounce_rate: 92.27 
          },
          { 
            page: 'Contact Page', 
            views: 677, 
            landing_page: 6278, 
            exit_page: 6537, 
            bounce_rate: 80.93 
          },
          { 
            page: 'About Us Page', 
            views: 640, 
            landing_page: 6117, 
            exit_page: 6386, 
            bounce_rate: 80.77 
          }
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
            <th>Page Name</th>
            <th>Total Views</th>
            <th>Landing Page</th>
            <th>Exit Page</th>
            <th>Bounce Rate %</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item, index) => (
            <tr key={index}>
              <td>{item.page}</td>
              <td>{item.views.toLocaleString()}</td>
              <td>{item.landing_page.toLocaleString()}</td>
              <td>{item.exit_page.toLocaleString()}</td>
              <td>{item.bounce_rate.toFixed(2)}%</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default PagesPerformanceTable;