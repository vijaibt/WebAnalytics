# PowerShell script to create React component files

# Create directories if they don't exist
$directories = @(
    "src/components/dashboard",
    "src/components/charts",
    "src/components/tables",
    "src/services",
    "src/pages"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force
        Write-Host "Created directory: $dir"
    }
}

# Define component templates
$reactComponentTemplate = @"
import React, { useState, useEffect } from 'react';
import '../../styles/components.css';

const COMPONENT_NAME = () => {
  // State and hooks
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch data or other initialization
    const fetchData = async () => {
      try {
        // Replace with actual API call
        setLoading(false);
      } catch (error) {
        console.error('Error fetching data:', error);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="component-container">
      <h2>COMPONENT_NAME</h2>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <div>
          {/* Component content goes here */}
        </div>
      )}
    </div>
  );
};

export default COMPONENT_NAME;
"@

$pageComponentTemplate = @"
import React from 'react';
import '../styles/pages.css';

const PAGE_NAME = () => {
  return (
    <div className="page-container">
      <h1>PAGE_NAME</h1>
      {/* Page content and components go here */}
    </div>
  );
};

export default PAGE_NAME;
"@

$serviceTemplate = @"
import api from './api';

// API service functions
const SERVICE_NAME = {
  // Define your API functions here
  getData: () => {
    return api.get('endpoint/');
  },
  
  // Add more functions as needed
};

export default SERVICE_NAME;
"@

$apiTemplate = @"
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;
"@

# Define files to create with their respective templates
$componentFiles = @(
    @{
        Path = "src/components/dashboard/DashboardLayout.js"
        Template = $reactComponentTemplate.Replace("COMPONENT_NAME", "DashboardLayout")
    },
    @{
        Path = "src/components/charts/VisitorsChart.js"
        Template = $reactComponentTemplate.Replace("COMPONENT_NAME", "VisitorsChart")
    },
    @{
        Path = "src/components/dashboard/UserMetricsCards.js"
        Template = $reactComponentTemplate.Replace("COMPONENT_NAME", "UserMetricsCards")
    },
    @{
        Path = "src/components/charts/GeographyTable.js"
        Template = $reactComponentTemplate.Replace("COMPONENT_NAME", "GeographyTable")
    },
    @{
        Path = "src/components/charts/PlatformChart.js"
        Template = $reactComponentTemplate.Replace("COMPONENT_NAME", "PlatformChart")
    },
    @{
        Path = "src/components/dashboard/SessionMetrics.js"
        Template = $reactComponentTemplate.Replace("COMPONENT_NAME", "SessionMetrics")
    },
    @{
        Path = "src/components/tables/SourcesTable.js"
        Template = $reactComponentTemplate.Replace("COMPONENT_NAME", "SourcesTable")
    },
    @{
        Path = "src/components/dashboard/PageMetrics.js"
        Template = $reactComponentTemplate.Replace("COMPONENT_NAME", "PageMetrics")
    },
    @{
        Path = "src/components/tables/PagesPerformanceTable.js"
        Template = $reactComponentTemplate.Replace("COMPONENT_NAME", "PagesPerformanceTable")
    },
    @{
        Path = "src/pages/Dashboard.js"
        Template = $pageComponentTemplate.Replace("PAGE_NAME", "Dashboard")
    },
    @{
        Path = "src/pages/EventsPage.js"
        Template = $pageComponentTemplate.Replace("PAGE_NAME", "EventsPage")
    },
    @{
        Path = "src/pages/SettingsPage.js"
        Template = $pageComponentTemplate.Replace("PAGE_NAME", "SettingsPage")
    },
    @{
        Path = "src/services/analyticsService.js"
        Template = $serviceTemplate.Replace("SERVICE_NAME", "analyticsService")
    },
    @{
        Path = "src/services/api.js"
        Template = $apiTemplate
    }
)

# Create each file
foreach ($file in $componentFiles) {
    if (-not (Test-Path $file.Path)) {
        Set-Content -Path $file.Path -Value $file.Template
        Write-Host "Created file: $file.Path"
    } else {
        Write-Host "File already exists: $file.Path"
    }
}

# Create CSS files
$cssFiles = @(
    "src/styles/components.css",
    "src/styles/pages.css"
)

foreach ($cssFile in $cssFiles) {
    if (-not (Test-Path $cssFile)) {
        New-Item -ItemType Directory -Path (Split-Path $cssFile) -Force
        Set-Content -Path $cssFile -Value "/* Styles for components */"
        Write-Host "Created CSS file: $cssFile"
    }
}

Write-Host "All files created successfully!"