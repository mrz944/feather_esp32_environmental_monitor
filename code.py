import time
import board
import busio
import json
import wifi
import socketpool
import displayio
import terminalio

from adafruit_display_text import label
from adafruit_httpserver import Server, Request, Response, GET, FileResponse
from collections import deque
from wifi_config import WIFI_SSID, WIFI_PASSWORD, SERVER_PORT

from circuitpython_sensirion_i2c_sen5x import Sen5xI2cDevice
from circuitpython_sensirion_i2c_driver import I2cTransceiver,I2cConnection

# Initialize display
display = board.DISPLAY
main_group = displayio.Group()
display.root_group = main_group

# Create text labels for display
# Create text labels with just the required positional arguments
title_label = label.Label(
    terminalio.FONT,
    text="SEN55 Sensor",
    anchor_point=(0.5, 0),
    anchored_position=(display.width // 2, 10)
)

readings_label = label.Label(
    terminalio.FONT,
    text="",
    x=10,
    y=40,
    line_spacing=1.2
)

status_label = label.Label(
    terminalio.FONT,
    text="Starting...",
    x=10,
    y=display.height - 20
)

main_group.append(title_label)
main_group.append(readings_label)
main_group.append(status_label)

# Initialize I2C for SEN55
i2c = board.I2C()
SEN55_ADDR = 0x69  # SEN55 I2C address
transceiver = I2cTransceiver(i2c, SEN55_ADDR)
sen5x_device = Sen5xI2cDevice(I2cConnection(transceiver))

# Data storage (1 hour of data with 5-minute intervals = 12 points)
MAX_HISTORY = 12
history = {
    'timestamps': deque([], MAX_HISTORY),
    'temperature': deque([], MAX_HISTORY),
    'humidity': deque([], MAX_HISTORY),
    'pm25': deque([], MAX_HISTORY),
    'pm10': deque([], MAX_HISTORY),
    'voc': deque([], MAX_HISTORY),
    'nox': deque([], MAX_HISTORY)
}

current_data = {
    'temperature': 0,
    'humidity': 0,
    'pm25': 0,
    'pm10': 0,
    'voc': 0,
    'nox': 0
}

def sen55_read_data():
    """Read measurement data from SEN55"""

    # Start measurement
    sen5x_device.start_measurement()

    time.sleep(3)

    for i in range(3):
        # Wait until next result is available
        print("Waiting for new data...")
        while sen5x_device.read_data_ready() is False:
            time.sleep(0.1)

        # Read measured values -> clears the "data ready" flag
        values = sen5x_device.read_measured_values()
        print(values)

        # Read device status
        status = sen5x_device.read_device_status()
        print("Device Status: {}\n".format(status))

    # Stop measurement
    sen5x_device.stop_measurement()

    # mc_1p0 = values.mass_concentration_1p0.physical
    mc_2p5 = values.mass_concentration_2p5.physical
    # mc_4p0 = values.mass_concentration_4p0.physical
    mc_10p0 = values.mass_concentration_10p0.physical
    ambient_rh = values.ambient_humidity.percent_rh
    ambient_t = values.ambient_temperature.degrees_celsius
    voc_index = values.voc_index.scaled
    nox_index = values.nox_index.scaled

    return ambient_t, ambient_rh, mc_2p5, mc_10p0, voc_index, nox_index

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
    return FileResponse(request, "index.html")

@server.route("/api/data")
def get_data(request: Request):
    """Return current and historical sensor data"""
    response_data = json.dumps({
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
    })
    response = Response(request, response_data)
    response.content_type = 'application/json'
    return response

# Start the sensor
try:
    sen5x_device.device_reset()
    sen5x_device.get_product_name()
    status_label.text = "Sensor initialized"
except Exception as e:
    status_label.text = "Sensor init failed!"
    print("Error initializing sensor: {}".format(e))

# Start the server
server.start(str(wifi.radio.ipv4_address), port=SERVER_PORT)
print("Server started on port {}".format(SERVER_PORT))

# Main loop
last_update = 0
update_interval = 300  # 5 min in seconds

while True:
    current_time = time.monotonic()
    
    # Update sensor data every 5 minutes
    if current_time - last_update >= update_interval:
        if collect_sensor_data():
            last_update = current_time
    
    # Handle any pending server requests
    server.poll()
