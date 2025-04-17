# Adafruit Feather ESP32-S3 TFT with SEN55 Environmental Monitor based od CircuitPython

This project uses an Adafruit Feather ESP32-S3 TFT board with a Sensirion SEN55 environmental sensor to monitor:
- Temperature
- Humidity
- Particulate Matter (PM2.5 and PM10)
- VOC Index
- NOx Index

The readings are displayed both on the TFT screen and served via a web interface with historical data graphs.

## Hardware Requirements

- Adafruit Feather ESP32-S3 TFT board
- Sensirion SEN55 Environmental Sensor
- USB-C cable for power and programming

## Software Requirements

- CircuitPython 9.x
- Required libraries (included in /lib):
  - adafruit_display_text
  - adafruit_httpserver
  - adafruit_bus_device
  - adafruit_datetime

## Setup Instructions

1. Connect the SEN55 sensor to the ESP32-S3 board:
   - VCC → 3.3V
   - GND → GND
   - SDA → SDA (GPIO3)
   - SCL → SCL (GPIO4)

2. Copy the project files to your ESP32-S3 board:
   ```
   /code.py
   /wifi_config.py
   /lib/
   /static/
   ```

3. Create a `wifi_config.py` file with your WiFi credentials:
   ```python
   WIFI_SSID = "your_wifi_ssid"
   WIFI_PASSWORD = "your_wifi_password"
   SERVER_PORT = 1234
   ```

4. The device will automatically:
   - Connect to WiFi
   - Initialize the SEN55 sensor
   - Start the web server
   - Begin collecting data every 5 minutes

## Web Interface

The web interface is available at `http://<device-ip>` and provides:
- Current sensor readings
- Historical data graphs for the last hour (12 data points at 5-minute intervals)
- Auto-refreshing data every 5 minutes

## Project Structure

- `code.py`: Main CircuitPython code
- `wifi_config.py`: WiFi configuration
- `static/`: Web interface files
  - `index.html`: Main webpage
  - `style.css`: Styling
  - `script.js`: JavaScript for graphs and data handling
- `lib/`: Required CircuitPython libraries

## Development

The project uses git for version control. To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License
