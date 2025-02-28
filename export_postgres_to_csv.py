import psycopg2
import csv
import os

# Database connection parameters - update these with your actual values
DB_NAME = "analytics"
DB_USER = "postgres"
DB_PASSWORD = "Podadai@123"  # Replace with your actual password
DB_HOST = "localhost"
DB_PORT = "5432"

# Output file path
OUTPUT_FILE = "events_data.csv"

# SQL query to fetch the data
QUERY = """
SELECT 
    event_name, received_at, timestamp, url, path, referrer, title,
    utm_source, utm_medium, utm_campaign, country, region
FROM 
    events
ORDER BY 
    timestamp DESC;
"""

def export_data():
    """Export data from PostgreSQL to CSV file."""
    try:
        # Connect to the database
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        
        # Create a cursor
        cursor = conn.cursor()
        
        # Execute the query
        cursor.execute(QUERY)
        
        # Get the column names
        column_names = [desc[0] for desc in cursor.description]
        
        # Fetch all rows
        rows = cursor.fetchall()
        
        # Write to CSV
        with open(OUTPUT_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            
            # Write header
            writer.writerow(column_names)
            
            # Write data rows
            writer.writerows(rows)
        
        print(f"Successfully exported {len(rows)} rows to {OUTPUT_FILE}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # Close the database connection
        if conn:
            cursor.close()
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    export_data()