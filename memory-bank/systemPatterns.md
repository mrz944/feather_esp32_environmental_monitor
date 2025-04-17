# System Patterns: ESP32-S3 with SEN55 Environmental Monitor

## System Architecture

The ESP32-S3 with SEN55 Environmental Monitor follows a layered architecture that integrates hardware components, data processing, storage, and presentation layers. The system is designed to be self-contained, requiring minimal external dependencies while providing robust functionality.

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      ESP32-S3 Device                        │
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────┐  │
│  │ SEN55       │    │ Data        │    │ TFT Display     │  │
│  │ Sensor      │───▶│ Processing  │───▶│ Interface       │  │
│  │ Interface   │    │ & Storage   │    │                 │  │
│  └─────────────┘    └──────┬──────┘    └─────────────────┘  │
│                            │                                │
│                     ┌──────▼──────┐                         │
│                     │ Web Server  │                         │
│                     │ & API       │                         │
│                     └──────┬──────┘                         │
└───────────────────────────┼─────────────────────────────────┘
                            │
                  ┌─────────▼─────────┐
                  │ Client Web Browser │
                  └───────────────────┘
```

## Key Technical Decisions

### 1. CircuitPython as the Runtime Environment
- **Decision**: Use CircuitPython 9.x as the programming environment
- **Rationale**: 
  - Simplified Python-based development experience
  - Rich library ecosystem for hardware interaction
  - Built-in support for file systems and web servers
  - Easier maintenance and updates compared to C/C++ alternatives

### 2. Data Storage Strategy
- **Decision**: Store historical data in CSV format on the device's filesystem
- **Rationale**:
  - Simple, human-readable format
  - Easy to process and parse
  - Compatible with CircuitPython's file handling
  - Allows for data persistence across power cycles
  - Enables potential export for external analysis

### 3. Web Interface Implementation
- **Decision**: Use client-side rendering with Chart.js for data visualization
- **Rationale**:
  - Minimizes server-side processing on the resource-constrained ESP32
  - Provides rich, interactive visualizations
  - Enables responsive design for different device sizes
  - Allows for client-side filtering and data manipulation

### 4. Sensor Reading Frequency
- **Decision**: Collect data at 5-minute intervals
- **Rationale**:
  - Balances data granularity with storage constraints
  - Sufficient for tracking environmental changes
  - Reduces power consumption compared to more frequent readings
  - Aligns with typical environmental monitoring practices

## Design Patterns

### 1. Producer-Consumer Pattern
- The SEN55 sensor (producer) generates environmental data
- The data processing module (consumer) processes and stores this data
- Implementation uses a scheduled polling approach rather than interrupts

### 2. MVC (Model-View-Controller) Pattern
- **Model**: Data storage in CSV and in-memory structures
- **View**: TFT display and web interface
- **Controller**: Main CircuitPython code handling logic and coordination

### 3. Observer Pattern
- The web server observes the data model
- When clients request data, they receive the current state
- Auto-refresh mechanism allows clients to observe changes over time

### 4. Repository Pattern
- Abstraction layer between data storage (CSV) and application logic
- Functions for loading, saving, and querying historical data

## Component Relationships

### Hardware Components
- **ESP32-S3 TFT Board**: Central controller with built-in display
- **SEN55 Sensor**: Connected via I2C for environmental measurements
- **Connection**: SDA (GPIO3) and SCL (GPIO4) pins with 3.3V power

### Software Components
1. **Sensor Interface Layer**
   - Handles communication with SEN55 via I2C
   - Manages sensor initialization, measurement cycles, and data reading
   - Implements error handling for sensor communication

2. **Data Management Layer**
   - Processes raw sensor readings
   - Maintains in-memory data structures (deques) for current session
   - Handles CSV file operations for persistent storage
   - Implements data retention policies (30-day history)

3. **Display Interface Layer**
   - Manages the TFT display
   - Updates readings at regular intervals
   - Provides status information to the user

4. **Web Server Layer**
   - Serves static HTML, CSS, and JavaScript files
   - Provides API endpoint for current and historical data
   - Handles HTTP requests and responses

## Critical Implementation Paths

### 1. Sensor Data Collection Path
```
SEN55 Initialization → Start Measurement → Read Data Ready Flag → 
Read Measured Values → Process Values → Update Current Data → 
Store in History → Update Display → Save to CSV
```

### 2. Web Interface Data Flow
```
Client Request → Server Receives Request → 
Server Retrieves Current and Historical Data → 
Server Formats JSON Response → Client Renders Data → 
Client Updates Charts and Displays
```

### 3. System Initialization Sequence
```
Initialize Display → Initialize I2C → Create Data Structures → 
Connect to WiFi → Initialize SEN55 Sensor → Load Historical Data → 
Start Web Server → Enter Main Loop
```

## Error Handling and Resilience

- Sensor communication errors are caught and logged
- WiFi connection issues are reported on the TFT display
- CSV file operations have error handling to prevent data corruption
- Memory management includes periodic garbage collection
- The system continues operation even if some components fail
