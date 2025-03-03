import React, { useState } from 'react';
import VisitorsChart from '../components/charts/VisitorsChart';
import UserMetricsCards from '../components/dashboard/UserMetricsCards';
import GeographyTable from '../components/charts/GeographyTable';
import PlatformChart from '../components/charts/PlatformChart';
import SessionMetrics from '../components/dashboard/SessionMetrics';
import SourcesTable from '../components/tables/SourcesTable';
import PageMetrics from '../components/dashboard/PageMetrics';
import PagesPerformanceTable from '../components/tables/PagesPerformanceTable';
import '../styles/pages.css';

const Dashboard = () => {
  const [timeRange, setTimeRange] = useState('7D');
  
  const handleTimeRangeChange = (range) => {
    setTimeRange(range);
  };
  
  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Web Analytics Dashboard</h1>
        <div className="time-range-buttons">
          <button onClick={() => handleTimeRangeChange('Today')} className={timeRange === 'Today' ? 'active' : ''}>Today</button>
          <button onClick={() => handleTimeRangeChange('Yesterday')} className={timeRange === 'Yesterday' ? 'active' : ''}>Yesterday</button>
          <button onClick={() => handleTimeRangeChange('7D')} className={timeRange === '7D' ? 'active' : ''}>7D</button>
          <button onClick={() => handleTimeRangeChange('30D')} className={timeRange === '30D' ? 'active' : ''}>30D</button>
          <button onClick={() => handleTimeRangeChange('3M')} className={timeRange === '3M' ? 'active' : ''}>3M</button>
        </div>
      </header>
      
      <section className="dashboard-section">
        <h2>User Metrics</h2>
        <UserMetricsCards timeRange={timeRange} />
        <VisitorsChart timeRange={timeRange} />
      </section>
      
      <div className="dashboard-row">
        <section className="dashboard-column">
          <h2>Geography</h2>
          <GeographyTable timeRange={timeRange} />
        </section>
        <section className="dashboard-column">
          <h2>Platform</h2>
          <PlatformChart timeRange={timeRange} />
        </section>
      </div>
      
      <section className="dashboard-section">
        <h2>Session Metrics</h2>
        <SessionMetrics timeRange={timeRange} />
      </section>
      
      <section className="dashboard-section">
        <h2>Traffic Sources</h2>
        <SourcesTable timeRange={timeRange} />
      </section>
      
      <section className="dashboard-section">
        <h2>Page Metrics</h2>
        <PageMetrics timeRange={timeRange} />
        <PagesPerformanceTable timeRange={timeRange} />
      </section>
    </div>
  );
};

export default Dashboard;