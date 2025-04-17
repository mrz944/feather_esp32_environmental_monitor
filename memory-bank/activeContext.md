# Active Context: ESP32-S3 with SEN55 Environmental Monitor

## Current Work Focus

The ESP32-S3 with SEN55 Environmental Monitor project is currently in a functional state with all core features implemented. The system successfully:

1. Collects environmental data from the SEN55 sensor
2. Displays readings on the TFT screen
3. Stores historical data in CSV format
4. Serves a web interface with current readings and historical charts
5. Allows date-based filtering of historical data

The current focus is on:
- Ensuring long-term stability and reliability
- Optimizing memory usage for extended operation
- Enhancing the web interface for better user experience
- Documenting the system for users and future developers

## Recent Changes

### Core Functionality
- Implemented 30-day rolling data storage with CSV persistence
- Added date range selection in the web interface
- Optimized sensor reading process for reliability
- Implemented periodic garbage collection to prevent memory leaks

### Web Interface
- Enhanced chart visualization with Chart.js
- Added responsive design for mobile and desktop viewing
- Implemented quick date range selection buttons
- Added connection status indicator

### System Stability
- Added error handling for sensor communication failures
- Implemented CSV file error recovery
- Added status display on TFT screen for system monitoring

## Next Steps

### Short-term Priorities
1. **Memory Optimization**
   - Review and optimize data structures
   - Implement more aggressive garbage collection if needed
   - Monitor memory usage over extended periods

2. **Data Validation**
   - Add validation for sensor readings to filter anomalies
   - Implement data integrity checks for CSV storage

3. **User Experience Improvements**
   - Add data export functionality to the web interface
   - Implement alert thresholds for environmental parameters
   - Add visual indicators for air quality status

### Medium-term Goals
1. **Extended Analytics**
   - Add statistical analysis of environmental trends
   - Implement daily/weekly/monthly averages
   - Create correlation views between different parameters

2. **System Enhancements**
   - Add optional cloud backup for historical data
   - Implement OTA (Over-The-Air) updates
   - Add power management for battery operation

3. **Additional Features**
   - Email or push notifications for threshold violations
   - Integration with home automation systems
   - Additional sensor support (e.g., CO2)

## Active Decisions and Considerations

### Data Storage Strategy
- **Current Approach**: CSV file with in-memory deque structures
- **Considerations**:
  - CSV provides human-readable format and easy parsing
  - In-memory structures provide fast access but are limited by RAM
  - 30-day retention balances historical data needs with storage constraints
- **Open Questions**:
  - Is compression needed for longer data retention?
  - Should we implement a database solution for more complex queries?

### Sensor Reading Frequency
- **Current Approach**: 5-minute intervals
- **Considerations**:
  - Balances data granularity with power and storage efficiency
  - Aligns with typical environmental monitoring practices
  - Provides sufficient resolution for trend analysis
- **Open Questions**:
  - Should frequency be user-configurable?
  - Would adaptive sampling based on rate of change be beneficial?

### Web Interface Design
- **Current Approach**: Client-side rendering with Chart.js
- **Considerations**:
  - Minimizes server-side processing on the ESP32
  - Provides rich visualization capabilities
  - Allows client-side filtering and manipulation
- **Open Questions**:
  - Would server-side data aggregation improve performance?
  - Should we implement data caching for faster chart rendering?

## Important Patterns and Preferences

### Code Organization
- Modular functions with clear responsibilities
- Error handling at appropriate levels
- Comments for complex logic and algorithms
- Consistent naming conventions

### Data Management
- Prefer fixed-size data structures to prevent memory issues
- Implement data validation before storage
- Use appropriate data types for memory efficiency
- Implement periodic cleanup and maintenance

### User Interface
- Clean, minimalist design
- Responsive layouts for different devices
- Clear visual hierarchy for information
- Intuitive controls and interactions

## Learnings and Project Insights

### Technical Insights
- CircuitPython's memory management requires careful attention for long-running applications
- The SEN55 sensor requires a warm-up period for accurate readings
- Web server performance on ESP32-S3 is adequate for basic interfaces but requires optimization for complex operations
- CSV is an efficient format for time-series data on resource-constrained devices

### User Experience Insights
- Environmental data is most valuable when presented with context and trends
- Users prefer visual representations over raw numbers
- Date range selection is essential for analyzing environmental patterns
- Connection status indicators are important for IoT devices

### Development Process Insights
- Incremental development with regular testing is essential
- Hardware and software testing should be integrated
- Documentation should be maintained alongside development
- Error handling is critical for autonomous IoT devices
