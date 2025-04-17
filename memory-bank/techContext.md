# Technical Context: ESP32-S3 with SEN55 Environmental Monitor

## Technologies Used

### Hardware Components

#### 1. Adafruit Feather ESP32-S3 TFT
- **Microcontroller**: ESP32-S3 dual-core processor
- **Memory**: 8MB Flash, 2MB PSRAM
- **Display**: Built-in 1.14" TFT display (240x135 pixels)
- **Connectivity**: WiFi and Bluetooth
- **Power**: USB-C or LiPo battery compatible
- **GPIO**: Multiple GPIO pins including I2C, SPI, UART
- **Features**: Built-in RGB NeoPixel, STEMMA QT connector

#### 2. Sensirion SEN55 Environmental Sensor
- **Measurements**:
  - Particulate Matter (PM1.0, PM2.5, PM4.0, PM10)
  - Temperature (-10 to +60 °C)
  - Humidity (0 to 100% RH)
  - VOC Index (1 to 500)
  - NOx Index (1 to 500)
- **Interface**: I2C
- **Address**: 0x69
- **Features**: 
  - Integrated fan for active air sampling
  - Self-cleaning technology
  - Long-term stability

### Software Stack

#### 1. CircuitPython 9.x
- **Language**: Python 3 variant optimized for microcontrollers
- **Features**:
  - USB drive file access
  - Interactive REPL
  - Native USB support
  - Built-in modules for hardware interaction

#### 2. Core Libraries
- **adafruit_display_text**: Text rendering on displays
- **adafruit_httpserver**: HTTP server implementation
- **adafruit_bus_device**: I2C and SPI device communication
- **adafruit_datetime**: Date and time handling

#### 3. Sensor Libraries
- **circuitpython_sensirion_i2c_driver**: Base driver for Sensirion I2C devices
- **circuitpython_sensirion_i2c_sen5x**: SEN5x specific implementation

#### 4. Web Technologies
- **HTML/CSS**: Static web interface structure and styling
- **JavaScript**: Client-side logic and data visualization
- **Chart.js**: JavaScript library for interactive charts
- **JSON**: Data exchange format between server and client

## Development Environment

### Hardware Setup
```
┌─────────────────────┐      ┌─────────────────┐
│ ESP32-S3 TFT Board  │      │ SEN55 Sensor    │
│                     │      │                 │
│  3.3V ─────────────────────► VCC             │
│  GND ──────────────────────► GND             │
│  GPIO3/SDA ─────────────────► SDA            │
│  GPIO4/SCL ─────────────────► SCL            │
└─────────────────────┘      └─────────────────┘
```

### Software Development Workflow
1. Edit code on computer
2. Save to ESP32-S3 (appears as USB drive)
3. Device automatically reloads with new code
4. View output via serial console if needed

### Project File Structure
```
/
├── code.py                 # Main application code
├── wifi_config.py          # WiFi credentials and configuration
├── lib/                    # Libraries
│   ├── adafruit_display_text/
│   ├── adafruit_httpserver/
│   ├── adafruit_bus_device/
│   ├── adafruit_datetime.mpy
│   ├── adafruit_logging.mpy
│   ├── circuitpython_sensirion_i2c_driver/
│   └── circuitpython_sensirion_i2c_sen5x/
├── static/                 # Web interface files
│   ├── index.html
│   ├── style.css
│   └── script.js
└── data/                   # Created at runtime
    └── sensor_history.csv  # Historical sensor data
```

## Technical Constraints

### Hardware Limitations

1. **Processing Power**
   - ESP32-S3 is powerful for a microcontroller but limited compared to full computers
   - Complex operations must be optimized or offloaded to the client

2. **Memory Constraints**
   - Limited RAM requires careful memory management
   - Use of deque data structures with fixed maximum sizes
   - Periodic garbage collection to prevent memory leaks

3. **Storage Limitations**
   - Limited flash storage space for historical data
   - CSV format chosen for efficiency and simplicity
   - 30-day rolling data retention policy to manage storage

4. **Power Considerations**
   - Designed primarily for continuous USB power
   - Battery operation possible but with reduced longevity due to WiFi and sensor fan

### Software Limitations

1. **CircuitPython Constraints**
   - Single-threaded execution model
   - Limited standard library compared to full Python
   - No support for certain advanced Python features

2. **Web Server Capabilities**
   - Basic HTTP server without HTTPS support
   - Limited concurrent connection handling
   - No advanced features like WebSockets

3. **Sensor Limitations**
   - 5-minute minimum interval between readings for accuracy
   - Warm-up period required for accurate readings
   - Temperature readings affected by device self-heating

## Dependencies and External Resources

### Required Libraries
- All required libraries are included in the `/lib` directory
- No external API dependencies

### External Resources
- Chart.js loaded from CDN for visualization
- No other external dependencies

## Tool Usage Patterns

### Development Tools
- CircuitPython compatible editor (Mu, VS Code, etc.)
- Serial console for debugging
- Web browser for interface testing

### Deployment Process
1. Install CircuitPython 9.x on the ESP32-S3 board
2. Copy all project files to the board
3. Create and configure wifi_config.py
4. Reset the device to start the application

### Maintenance Procedures
- Monitor serial output for errors
- Check CSV data periodically for integrity
- Update CircuitPython libraries as needed

### Debugging Approaches
- Serial console output for runtime information
- Status display on TFT screen
- Web interface connection status indicator
- Error logging in code
