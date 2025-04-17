# ESP32-S3 with SEN55 Environmental Monitor Project Brief

## Project Overview
This project combines an Adafruit Feather ESP32-S3 TFT board with a Sensirion SEN55 environmental sensor to create a comprehensive environmental monitoring solution. The system continuously monitors key air quality and environmental parameters and presents them through both a local TFT display and a web interface.

## Core Requirements

### Hardware Requirements
- Adafruit Feather ESP32-S3 TFT board as the main controller
- Sensirion SEN55 Environmental Sensor for data collection
- USB-C connection for power and programming

### Sensor Parameters to Monitor
- Temperature (°C)
- Humidity (%)
- Particulate Matter 2.5 (PM2.5) in μg/m³
- Particulate Matter 10 (PM10) in μg/m³
- Volatile Organic Compounds (VOC) Index
- Nitrogen Oxides (NOx) Index

### Display Methods
1. **TFT Display**: Real-time display of current sensor readings on the ESP32-S3's built-in TFT screen
2. **Web Interface**: A responsive web dashboard accessible via the device's IP address showing:
   - Current readings in an easy-to-read format
   - Historical data visualized through interactive charts
   - Date range selection for viewing historical trends

### Data Management
- Collect sensor readings at 5-minute intervals
- Store historical data in a CSV file on the device
- Maintain up to 30 days of historical data (8,640 data points)
- Provide API endpoint for accessing current and historical data

### Connectivity
- Connect to local WiFi network using credentials stored in configuration file
- Serve web interface via HTTP server
- Auto-refresh data on the web interface every 30 seconds

## Project Goals
1. Create a reliable, accurate environmental monitoring system
2. Provide easy access to current environmental data
3. Enable analysis of environmental trends over time
4. Make the system accessible to users without technical knowledge
5. Ensure the system operates continuously with minimal maintenance

## Success Criteria
- Accurate sensor readings matching Sensirion SEN55 specifications
- Reliable data collection and storage
- Responsive and intuitive web interface
- Stable operation over extended periods
- Clear visualization of environmental trends
