from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from datetime import datetime
import platform
import random

app = FastAPI(
    title="SCADA Monitoring System",
    description="Industrial SCADA application for machine monitoring and control",
    version="1.0.0"
)

# Simulated machine state
machine_state = {
    "running": True,
    "speed": 75.0,
    "temperature": 68.5,
    "pressure": 4.2,
    "vibration": 0.8,
    "power": 85.0,
    "production_count": 0,
    "error_count": 0,
    "last_maintenance": "2025-12-01",
    "uptime_hours": 245.5
}


@app.get("/", response_class=HTMLResponse)
async def home():
    """SCADA Dashboard - Main monitoring interface"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SCADA Monitoring System</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: #0a0e27;
                color: #fff;
                padding: 20px;
            }
            .header {
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                padding: 20px 30px;
                border-radius: 10px;
                margin-bottom: 20px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            }
            .header h1 {
                font-size: 2em;
                margin-bottom: 5px;
            }
            .header .subtitle {
                color: #b3d4fc;
                font-size: 0.9em;
            }
            .dashboard {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin-bottom: 20px;
            }
            .card {
                background: linear-gradient(135deg, #1a1f3a 0%, #2d3561 100%);
                border-radius: 10px;
                padding: 25px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
                border: 1px solid #2a5298;
            }
            .card h3 {
                color: #4a9eff;
                margin-bottom: 15px;
                font-size: 1.1em;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            .machine-visual {
                grid-column: 1 / -1;
                text-align: center;
                padding: 30px;
            }
            .machine-icon {
                font-size: 120px;
                margin-bottom: 20px;
                animation: pulse 2s infinite;
            }
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.7; }
            }
            .machine-status {
                font-size: 1.5em;
                font-weight: bold;
                margin-top: 10px;
            }
            .status-running { color: #10b981; }
            .status-stopped { color: #ef4444; }
            .status-warning { color: #f59e0b; }
            
            .indicator {
                margin-bottom: 20px;
            }
            .indicator-label {
                display: flex;
                justify-content: space-between;
                margin-bottom: 8px;
                font-size: 0.9em;
            }
            .indicator-value {
                font-size: 1.8em;
                font-weight: bold;
                color: #4a9eff;
            }
            .indicator-unit {
                font-size: 0.8em;
                color: #b3d4fc;
                margin-left: 5px;
            }
            .progress-bar {
                width: 100%;
                height: 12px;
                background: #0a0e27;
                border-radius: 10px;
                overflow: hidden;
                margin-top: 8px;
            }
            .progress-fill {
                height: 100%;
                background: linear-gradient(90deg, #4a9eff 0%, #00d4ff 100%);
                transition: width 0.5s ease;
                border-radius: 10px;
            }
            .progress-fill.warning {
                background: linear-gradient(90deg, #f59e0b 0%, #fbbf24 100%);
            }
            .progress-fill.danger {
                background: linear-gradient(90deg, #ef4444 0%, #f87171 100%);
            }
            
            .control-panel {
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
            }
            .btn {
                padding: 12px 24px;
                border: none;
                border-radius: 5px;
                font-size: 1em;
                cursor: pointer;
                transition: all 0.3s;
                font-weight: 600;
                flex: 1;
                min-width: 120px;
            }
            .btn-start {
                background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                color: white;
            }
            .btn-stop {
                background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
                color: white;
            }
            .btn-reset {
                background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
                color: white;
            }
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
            }
            .btn:disabled {
                opacity: 0.5;
                cursor: not-allowed;
                transform: none;
            }
            
            .stats-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 15px;
            }
            .stat-item {
                background: #0a0e27;
                padding: 15px;
                border-radius: 8px;
                text-align: center;
            }
            .stat-value {
                font-size: 1.5em;
                font-weight: bold;
                color: #4a9eff;
            }
            .stat-label {
                font-size: 0.8em;
                color: #b3d4fc;
                margin-top: 5px;
            }
            
            .alarm-panel {
                background: #1a0000;
                border: 2px solid #ef4444;
                padding: 15px;
                border-radius: 8px;
                display: none;
            }
            .alarm-panel.active {
                display: block;
                animation: blink 1s infinite;
            }
            @keyframes blink {
                0%, 50%, 100% { opacity: 1; }
                25%, 75% { opacity: 0.5; }
            }
            .alarm-text {
                color: #ef4444;
                font-weight: bold;
                text-align: center;
            }
            
            .timestamp {
                text-align: center;
                color: #b3d4fc;
                margin-top: 20px;
                font-size: 0.9em;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>⚙️ SCADA Monitoring System</h1>
            <p class="subtitle">Industrial Machine Control & Data Acquisition</p>
            <div class="timestamp" id="timestamp"></div>
        </div>

        <div class="dashboard">
            <!-- Machine Visual Status -->
            <div class="card machine-visual">
                <div class="machine-icon" id="machine-icon">🏭</div>
                <div class="machine-status" id="machine-status">Machine Running</div>
                <div id="alarm-panel" class="alarm-panel">
                    <div class="alarm-text">⚠️ ALARM: Critical Parameter Detected!</div>
                </div>
            </div>

            <!-- Speed Indicator -->
            <div class="card">
                <h3>⚡ Motor Speed</h3>
                <div class="indicator">
                    <div class="indicator-value">
                        <span id="speed-value">0</span>
                        <span class="indicator-unit">RPM</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" id="speed-bar"></div>
                    </div>
                </div>
                <div class="indicator-label">
                    <span>Target: 1500 RPM</span>
                    <span id="speed-percent">0%</span>
                </div>
            </div>

            <!-- Temperature Indicator -->
            <div class="card">
                <h3>🌡️ Temperature</h3>
                <div class="indicator">
                    <div class="indicator-value">
                        <span id="temp-value">0</span>
                        <span class="indicator-unit">°C</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" id="temp-bar"></div>
                    </div>
                </div>
                <div class="indicator-label">
                    <span>Max: 95°C</span>
                    <span id="temp-percent">0%</span>
                </div>
            </div>

            <!-- Pressure Indicator -->
            <div class="card">
                <h3>💨 Pressure</h3>
                <div class="indicator">
                    <div class="indicator-value">
                        <span id="pressure-value">0</span>
                        <span class="indicator-unit">bar</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" id="pressure-bar"></div>
                    </div>
                </div>
                <div class="indicator-label">
                    <span>Max: 6.5 bar</span>
                    <span id="pressure-percent">0%</span>
                </div>
            </div>

            <!-- Vibration Indicator -->
            <div class="card">
                <h3>📊 Vibration</h3>
                <div class="indicator">
                    <div class="indicator-value">
                        <span id="vibration-value">0</span>
                        <span class="indicator-unit">mm/s</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" id="vibration-bar"></div>
                    </div>
                </div>
                <div class="indicator-label">
                    <span>Max: 3.0 mm/s</span>
                    <span id="vibration-percent">0%</span>
                </div>
            </div>

            <!-- Power Consumption -->
            <div class="card">
                <h3>⚡ Power Consumption</h3>
                <div class="indicator">
                    <div class="indicator-value">
                        <span id="power-value">0</span>
                        <span class="indicator-unit">kW</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" id="power-bar"></div>
                    </div>
                </div>
                <div class="indicator-label">
                    <span>Max: 120 kW</span>
                    <span id="power-percent">0%</span>
                </div>
            </div>

            <!-- Production Statistics -->
            <div class="card">
                <h3>📈 Production Stats</h3>
                <div class="stats-grid">
                    <div class="stat-item">
                        <div class="stat-value" id="production-count">0</div>
                        <div class="stat-label">Units Produced</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value" id="error-count">0</div>
                        <div class="stat-label">Errors</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value" id="uptime">0.0</div>
                        <div class="stat-label">Uptime (hrs)</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value" id="efficiency">0</div>
                        <div class="stat-label">Efficiency %</div>
                    </div>
                </div>
            </div>

            <!-- Control Panel -->
            <div class="card">
                <h3>🎛️ Control Panel</h3>
                <div class="control-panel">
                    <button class="btn btn-start" id="btn-start" onclick="startMachine()">▶️ Start</button>
                    <button class="btn btn-stop" id="btn-stop" onclick="stopMachine()">⏹️ Stop</button>
                    <button class="btn btn-reset" onclick="resetCounters()">🔄 Reset</button>
                </div>
                <div style="margin-top: 15px; padding: 10px; background: #0a0e27; border-radius: 5px; font-size: 0.85em;">
                    <div>Last Maintenance: <span id="last-maintenance">2025-12-01</span></div>
                </div>
            </div>
        </div>

        <script>
            let machineRunning = false;
            let productionCount = 0;
            let errorCount = 0;
            let uptimeHours = 0;

            function updateTimestamp() {
                const now = new Date();
                document.getElementById('timestamp').textContent = 
                    'System Time: ' + now.toLocaleString();
            }

            function updateIndicator(id, value, max) {
                const percent = Math.min((value / max) * 100, 100);
                document.getElementById(id + '-value').textContent = value.toFixed(1);
                document.getElementById(id + '-percent').textContent = percent.toFixed(0) + '%';
                
                const bar = document.getElementById(id + '-bar');
                bar.style.width = percent + '%';
                
                // Color coding based on percentage
                bar.className = 'progress-fill';
                if (percent > 90) {
                    bar.classList.add('danger');
                } else if (percent > 75) {
                    bar.classList.add('warning');
                }
                
                return percent;
            }

            async function fetchMachineData() {
                try {
                    const response = await fetch('/api/machine/status');
                    const data = await response.json();
                    
                    machineRunning = data.running;
                    
                    // Update machine status
                    const statusEl = document.getElementById('machine-status');
                    const iconEl = document.getElementById('machine-icon');
                    const alarmEl = document.getElementById('alarm-panel');
                    
                    if (data.running) {
                        statusEl.textContent = 'Machine Running';
                        statusEl.className = 'machine-status status-running';
                        iconEl.style.animation = 'pulse 1s infinite';
                    } else {
                        statusEl.textContent = 'Machine Stopped';
                        statusEl.className = 'machine-status status-stopped';
                        iconEl.style.animation = 'none';
                    }
                    
                    // Update indicators
                    updateIndicator('speed', data.speed * 20, 1500); // Convert to RPM
                    const tempPercent = updateIndicator('temp', data.temperature, 95);
                    const pressurePercent = updateIndicator('pressure', data.pressure, 6.5);
                    const vibrationPercent = updateIndicator('vibration', data.vibration, 3.0);
                    updateIndicator('power', data.power, 120);
                    
                    // Check for alarms
                    if (tempPercent > 90 || pressurePercent > 90 || vibrationPercent > 85) {
                        alarmEl.classList.add('active');
                    } else {
                        alarmEl.classList.remove('active');
                    }
                    
                    // Update stats
                    document.getElementById('production-count').textContent = data.production_count;
                    document.getElementById('error-count').textContent = data.error_count;
                    document.getElementById('uptime').textContent = data.uptime_hours.toFixed(1);
                    
                    const efficiency = data.running ? Math.min(100, 60 + Math.random() * 35) : 0;
                    document.getElementById('efficiency').textContent = efficiency.toFixed(0);
                    
                    document.getElementById('last-maintenance').textContent = data.last_maintenance;
                    
                    // Update button states
                    document.getElementById('btn-start').disabled = data.running;
                    document.getElementById('btn-stop').disabled = !data.running;
                    
                } catch (error) {
                    console.error('Error fetching machine data:', error);
                }
            }

            async function startMachine() {
                await fetch('/api/machine/start', { method: 'POST' });
                fetchMachineData();
            }

            async function stopMachine() {
                await fetch('/api/machine/stop', { method: 'POST' });
                fetchMachineData();
            }

            async function resetCounters() {
                await fetch('/api/machine/reset', { method: 'POST' });
                fetchMachineData();
            }

            // Update every second
            updateTimestamp();
            setInterval(updateTimestamp, 1000);
            
            fetchMachineData();
            setInterval(fetchMachineData, 2000);
        </script>
    </body>
    </html>
    """
    return html_content


@app.get("/api/machine/status")
async def get_machine_status():
    """Get current machine status and all sensor readings"""
    # Simulate sensor fluctuations when running
    if machine_state["running"]:
        machine_state["speed"] = max(0, min(100, machine_state["speed"] + random.uniform(-3, 3)))
        machine_state["temperature"] = max(20, min(95, machine_state["temperature"] + random.uniform(-2, 2)))
        machine_state["pressure"] = max(0, min(6.5, machine_state["pressure"] + random.uniform(-0.3, 0.3)))
        machine_state["vibration"] = max(0, min(3, machine_state["vibration"] + random.uniform(-0.2, 0.2)))
        machine_state["power"] = max(0, min(120, machine_state["power"] + random.uniform(-5, 5)))
        machine_state["uptime_hours"] += 0.0006  # Increment uptime
        
        # Simulate production
        if random.random() > 0.7:
            machine_state["production_count"] += 1
        
        # Simulate occasional errors
        if random.random() > 0.95:
            machine_state["error_count"] += 1
    
    return machine_state


@app.post("/api/machine/start")
async def start_machine():
    """Start the machine"""
    machine_state["running"] = True
    machine_state["speed"] = 75.0
    machine_state["temperature"] = 68.5
    machine_state["pressure"] = 4.2
    machine_state["vibration"] = 0.8
    machine_state["power"] = 85.0
    return {"status": "Machine started", "timestamp": datetime.utcnow().isoformat()}


@app.post("/api/machine/stop")
async def stop_machine():
    """Stop the machine"""
    machine_state["running"] = False
    machine_state["speed"] = 0.0
    machine_state["power"] = 0.0
    return {"status": "Machine stopped", "timestamp": datetime.utcnow().isoformat()}


@app.post("/api/machine/reset")
async def reset_counters():
    """Reset production counters"""
    machine_state["production_count"] = 0
    machine_state["error_count"] = 0
    machine_state["uptime_hours"] = 0.0
    return {"status": "Counters reset", "timestamp": datetime.utcnow().isoformat()}


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "SCADA Monitoring System"
    }


@app.get("/api/info")
async def system_info():
    """System information endpoint"""
    return {
        "application": "SCADA Monitoring System",
        "version": "1.0.0",
        "python_version": platform.python_version(),
        "platform": platform.system(),
        "timestamp": datetime.utcnow().isoformat(),
        "machine_status": machine_state["running"]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
