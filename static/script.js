// Configuration
const UPDATE_INTERVAL = 5 * 60 * 1000; // 5 minutes in milliseconds
const MAX_DATA_POINTS = 12; // Store 1 hour of data (12 points at 5-minute intervals)

// Chart colors
const chartColors = {
    temperature: 'rgba(255, 99, 132, 0.7)',
    humidity: 'rgba(54, 162, 235, 0.7)',
    pm25: 'rgba(255, 206, 86, 0.7)',
    pm10: 'rgba(75, 192, 192, 0.7)',
    voc: 'rgba(153, 102, 255, 0.7)',
    nox: 'rgba(255, 159, 64, 0.7)'
};

// Data storage
let sensorData = {
    timestamps: [],
    temperature: [],
    humidity: [],
    pm25: [],
    pm10: [],
    voc: [],
    nox: []
};

// Chart objects
let charts = {
    temperature: null,
    humidity: null,
    particles: null,
    gases: null
};

// Initialize the page
document.addEventListener('DOMContentLoaded', () => {
    initCharts();
    fetchData();
    
    // Set up periodic updates
    setInterval(fetchData, UPDATE_INTERVAL);
});

// Initialize charts
function initCharts() {
    // Temperature chart
    charts.temperature = new Chart(
        document.getElementById('temperatureChart'),
        {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Temperature (°C)',
                    data: [],
                    borderColor: chartColors.temperature,
                    backgroundColor: chartColors.temperature.replace('0.7', '0.1'),
                    borderWidth: 2,
                    tension: 0.3,
                    pointRadius: 3
                }]
            },
            options: getChartOptions('Temperature over time')
        }
    );
    
    // Humidity chart
    charts.humidity = new Chart(
        document.getElementById('humidityChart'),
        {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Humidity (%)',
                    data: [],
                    borderColor: chartColors.humidity,
                    backgroundColor: chartColors.humidity.replace('0.7', '0.1'),
                    borderWidth: 2,
                    tension: 0.3,
                    pointRadius: 3
                }]
            },
            options: getChartOptions('Humidity over time')
        }
    );
    
    // Particles chart
    charts.particles = new Chart(
        document.getElementById('particlesChart'),
        {
            type: 'line',
            data: {
                labels: [],
                datasets: [
                    {
                        label: 'PM2.5 (μg/m³)',
                        data: [],
                        borderColor: chartColors.pm25,
                        backgroundColor: 'transparent',
                        borderWidth: 2,
                        tension: 0.3,
                        pointRadius: 3
                    },
                    {
                        label: 'PM10 (μg/m³)',
                        data: [],
                        borderColor: chartColors.pm10,
                        backgroundColor: 'transparent',
                        borderWidth: 2,
                        tension: 0.3,
                        pointRadius: 3
                    }
                ]
            },
            options: getChartOptions('Particulate Matter over time')
        }
    );
    
    // Gases chart
    charts.gases = new Chart(
        document.getElementById('gasesChart'),
        {
            type: 'line',
            data: {
                labels: [],
                datasets: [
                    {
                        label: 'VOC Index',
                        data: [],
                        borderColor: chartColors.voc,
                        backgroundColor: 'transparent',
                        borderWidth: 2,
                        tension: 0.3,
                        pointRadius: 3
                    },
                    {
                        label: 'NOx Index',
                        data: [],
                        borderColor: chartColors.nox,
                        backgroundColor: 'transparent',
                        borderWidth: 2,
                        tension: 0.3,
                        pointRadius: 3
                    }
                ]
            },
            options: getChartOptions('Gas Indices over time')
        }
    );
}

// Common chart options
function getChartOptions(title) {
    return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            title: {
                display: true,
                text: title,
                font: {
                    size: 16
                }
            },
            legend: {
                position: 'top'
            },
            tooltip: {
                mode: 'index',
                intersect: false
            }
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Time'
                }
            },
            y: {
                beginAtZero: false
            }
        }
    };
}

// Fetch data from the server
function fetchData() {
    fetch('/api/data')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            document.getElementById('connection-status').innerHTML = '🟢 Connected';
            return response.json();
        })
        .then(data => {
            updateCurrentReadings(data.current);
            updateHistoricalData(data.history);
            updateLastUpdateTime();
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            document.getElementById('connection-status').innerHTML = '🔴 Disconnected';
        });
}

// Update the current readings display
function updateCurrentReadings(data) {
    document.getElementById('temperature').textContent = data.temperature.toFixed(1);
    document.getElementById('humidity').textContent = data.humidity.toFixed(1);
    document.getElementById('pm25').textContent = data.pm25.toFixed(1);
    document.getElementById('pm10').textContent = data.pm10.toFixed(1);
    document.getElementById('voc').textContent = data.voc.toFixed(1);
    document.getElementById('nox').textContent = data.nox.toFixed(1);
}

// Update historical data and charts
function updateHistoricalData(history) {
    // Update our data storage
    sensorData = history;
    
    // Format timestamps for display
    const formattedLabels = sensorData.timestamps.map(timestamp => {
        const date = new Date(timestamp * 1000);
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    });
    
    // Update temperature chart
    charts.temperature.data.labels = formattedLabels;
    charts.temperature.data.datasets[0].data = sensorData.temperature;
    charts.temperature.update();
    
    // Update humidity chart
    charts.humidity.data.labels = formattedLabels;
    charts.humidity.data.datasets[0].data = sensorData.humidity;
    charts.humidity.update();
    
    // Update particles chart
    charts.particles.data.labels = formattedLabels;
    charts.particles.data.datasets[0].data = sensorData.pm25;
    charts.particles.data.datasets[1].data = sensorData.pm10;
    charts.particles.update();
    
    // Update gases chart
    charts.gases.data.labels = formattedLabels;
    charts.gases.data.datasets[0].data = sensorData.voc;
    charts.gases.data.datasets[1].data = sensorData.nox;
    charts.gases.update();
}

// Update the last update timestamp
function updateLastUpdateTime() {
    const now = new Date();
    const timeString = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    document.getElementById('last-update').textContent = `Last updated: ${timeString}`;
}
