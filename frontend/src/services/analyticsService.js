// In src/services/analyticsService.js
import api from './api';

const analyticsService = {
  // User metrics
  getDailyActiveUsers: (days = 30) => {
    return api.get(`analytics/daily/?days=${days}`);
  },
  
  getNewUsers: (days = 7) => {
    return api.get(`analytics/daily/?event_name=pageview&days=${days}`);
  },
  
  // Geography data
  getPageViewsByCountry: () => {
    return api.get('analytics/countries/');
  },
  
  // Platform data
  getPlatformData: () => {
    return api.get('analytics/top-pages/'); // You might need to create this endpoint
  },
  
  // Session metrics
  getSessionMetrics: (days = 30) => {
    return api.get(`events/?event_name=pageview&days=${days}`);
  },
  
  // Traffic sources
  getTrafficSources: () => {
    return api.get('analytics/daily/');
  },
  
  // Page metrics
  getPageMetrics: () => {
    return api.get('analytics/top-pages/');
  },
  
  // Pages performance
  getPagesPerformance: () => {
    return api.get('analytics/top-pages/');
  }
};

export default analyticsService;