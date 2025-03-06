// src/services/analyticsService.js
import api from './api';

const analyticsService = {
  // User metrics
  getDailyActiveUsers: (days = 7) => {
    return api.get(`analytics/daily/?days=${days}`);
  },
  
  getUniqueUsers: (days = 7) => {
    return api.get(`analytics/daily/?distinct=user_id&days=${days}`);
  },
  
  getNewUsers: (days = 7) => {
    return api.get(`analytics/daily/?new=true&days=${days}`);
  },
  
  // Geography data
  getPageViewsByCountry: (days = 7) => {
    return api.get(`analytics/countries/?days=${days}`);
  },
  
  // Platform data
  getPlatformData: (days = 7) => {
    return api.get(`analytics/platforms/?days=${days}`);
  },
  
  // Session metrics
  getSessionMetrics: (days = 7) => {
    return api.get(`analytics/sessions/?days=${days}`);
  },
  
  // Traffic sources
  getTrafficSources: (days = 7) => {
    return api.get(`analytics/sources/?days=${days}`);
  },
  
  // Page metrics
  getPageViews: (days = 7) => {
    return api.get(`analytics/pages/?days=${days}`);
  },
  
  getTopPages: (days = 7, limit = 10) => {
    return api.get(`analytics/top-pages/?days=${days}&limit=${limit}`);
  },
  
  // Raw events
  getEvents: (params = {}) => {
    return api.get('events/', { params });
  }
};

export default analyticsService;