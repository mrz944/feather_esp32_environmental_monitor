import time
import board
import busio
import json
import wifi
import socketpool
import displayio
import terminalio
from adafruit_display_text import label
from adafruit_httpserver import Server, Request, Response, GET
from collections import deque
from wifi_config import WIFI_SSID, WIFI_PASSWORD, SERVER_PORT

# Initialize display
display = board.DISPLAY
main_group = displayio.Group()
display.show(main_group)

# Create text labels for display
title_label = label.Label(
    terminalio.FONT,
    text="SEN55 Sensor",
    color=0xFFFFFF,
    x=display.width // 2,
    y=10,
    anchor_point=(0.5, 0),
    anchored_position=(display.width // 2, 10),
)

readings_label = label.Label(
    terminalio.FONT,
    text="",
    color=0xFFFFFF,
    x=10,
    y=40,
    line_spacing=1.2
)

status_label = label.Label(
    terminalio.FONT,
    text="Starting...",
    color=0xFFFFFF,
    x=10,
    y=display.height - 20
)

main_group.append(title_label)
main_group.append(readings_label)
main_group.append(status_label)

# Initialize I2C for SEN55
i2c = busio.I2C(board.SCL, board.SDA)
SEN55_ADDR = 0x69  # SEN55 I2C address

# Data storage (1 hour of data with 5-minute intervals = 12 points)
MAX_HISTORY = 12
history = {
    'timestamps': deque(maxlen=MAX_HISTORY),
    'temperature': deque(maxlen=MAX_HISTORY),
    'humidity': deque(maxlen=MAX_HISTORY),
    'pm25': deque(maxlen=MAX_HISTORY),
    'pm10': deque(maxlen=MAX_HISTORY),
    'voc': deque(maxlen=MAX_HISTORY),
    'nox': deque(maxlen=MAX_HISTORY)
}

current_data = {
    'temperature': 0,
    'humidity': 0,
    'pm25': 0,
    'pm10': 0,
    'voc': 0,
    'nox': 0
}

def sen55_start_measurement():
    """Start continuous measurement on SEN55"""
    try:
        i2c.try_lock()
        i2c.writeto(SEN55_ADDR, bytes([0x00, 0x21]))  # Start measurement command
    finally:
        i2c.unlock()
    time.sleep(0.1)  # Wait for command to process

def sen55_read_data():
    """Read measurement data from SEN55"""
    try:
        i2c.try_lock()
        # Read measured values command
        i2c.writeto(SEN55_ADDR, bytes([0x03, 0xC4]))
        time.sleep(0.02)  # Wait for data
        
        # Read 24 bytes of data
        result = bytearray(24)
        i2c.readfrom_into(SEN55_ADDR, result)
        
        # Parse data according to SEN55 data format
        pm25 = (result[0] << 8 | result[1]) / 10
        pm10 = (result[3] << 8 | result[4]) / 10
        humidity = (result[6] << 8 | result[7]) / 100
        temperature = (result[9] << 8 | result[10]) / 200
        voc = (result[12] << 8 | result[13]) / 10
        nox = (result[15] << 8 | result[16]) / 10
        
        return temperature, humidity, pm25, pm10, voc, nox
    finally:
        i2c.unlock()

def update_display():
    """Update the display with current sensor readings"""
    readings_text = "Temp: {:.1f}°C\nHumidity: {:.1f}%\nPM2.5: {:.1f} µg/m³\nPM10: {:.1f} µg/m³\nVOC: {:.1f}\nNOx: {:.1f}".format(
        current_data['temperature'],
        current_data['humidity'],
        current_data['pm25'],
        current_data['pm10'],
        current_data['voc'],
        current_data['nox']
    )
    readings_label.text = readings_text

def collect_sensor_data():
    """Collect data from sensor and update storage"""
    try:
        temp, hum, pm25, pm10, voc, nox = sen55_read_data()
        
        current_data.update({
            'temperature': temp,
            'humidity': hum,
            'pm25': pm25,
            'pm10': pm10,
            'voc': voc,
            'nox': nox
        })
        
        timestamp = time.time()
        history['timestamps'].append(timestamp)
        history['temperature'].append(temp)
        history['humidity'].append(hum)
        history['pm25'].append(pm25)
        history['pm10'].append(pm10)
        history['voc'].append(voc)
        history['nox'].append(nox)
        
        update_display()
        return True
    except Exception as e:
        print("Error collecting sensor data: {}".format(e))
        return False

# Connect to WiFi
status_label.text = "Connecting to WiFi..."
wifi.radio.connect(WIFI_SSID, WIFI_PASSWORD)
status_label.text = "IP: {}".format(wifi.radio.ipv4_address)

# Initialize HTTP server
pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/static", debug=True)

@server.route("/")
def base(request: Request):
    """Serve the main page"""
    return Response(request, file="static/index.html")

@server.route("/api/data")
def get_data(request: Request):
    """Return current and historical sensor data"""
    return Response(
        request,
        json.dumps({
            'current': current_data,
            'history': {
                'timestamps': list(history['timestamps']),
                'temperature': list(history['temperature']),
                'humidity': list(history['humidity']),
                'pm25': list(history['pm25']),
                'pm10': list(history['pm10']),
                'voc': list(history['voc']),
                'nox': list(history['nox'])
            }
        }),
        content_type='application/json'
    )

# Start the sensor
try:
    sen55_start_measurement()
    status_label.text = "Sensor initialized"
except Exception as e:
    status_label.text = "Sensor init failed!"
    print("Error initializing sensor: {}".format(e))

# Start the server
server.start(port=SERVER_PORT)
print("Server started on port {}".format(SERVER_PORT))

# Main loop
last_update = 0
update_interval = 300  # 5 minutes in seconds

while True:
    try:
        current_time = time.monotonic()
        
        # Update sensor data every 5 minutes
        if current_time - last_update >= update_interval:
            if collect_sensor_data():
                last_update = current_time
        
        # Handle any pending server requests
        server.poll()
        
    except Exception as e:
        print("Error in main loop: {}".format(e))
        time.sleep(1)
