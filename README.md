# SCADA Monitoring System

A mock SCADA (Supervisory Control and Data Acquisition) application for industrial machine monitoring and control, built with FastAPI and ready for Docker deployment.

## 🚀 Features

- **Real-time Machine Monitoring** - Live sensor data visualization
- **Interactive Dashboard** - Modern industrial-grade UI
- **Control Operations** - Start/Stop/Reset machine controls
- **Multiple Indicators**:
  - ⚡ Motor Speed (RPM)
  - 🌡️ Temperature (°C)
  - 💨 Pressure (bar)
  - 📊 Vibration (mm/s)
  - ⚡ Power Consumption (kW)
- **Production Statistics** - Track units produced, errors, uptime, and efficiency
- **Alarm System** - Visual and color-coded warnings for critical parameters
- **API Endpoints** - RESTful API for machine control and monitoring

## 📁 Project Structure

```
app_to_deploy/
├── app/
│   ├── __init__.py
│   └── main.py          # Main application file
├── Dockerfile           # Docker configuration
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🛠️ Local Development

### Prerequisites
- Python 3.11+
- Docker (for containerized deployment)

### Run Locally

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python -m app.main
```

3. Open your browser:
- SCADA Dashboard: http://localhost:8000
- API docs: http://localhost:8000/docs
- Machine status: http://localhost:8000/api/machine/status

## 🐳 Docker Deployment

### Build Docker Image

```bash
docker build -t fastapi-app .
```

### Run Docker Container

```bash
docker run -d -p 8000:8000 --name my-fastapi-app fastapi-app
```

### Check Container Status

```bash
docker ps
```

### View Logs

```bash
docker logs my-fastapi-app
```

### Stop Container

```bash
docker stop my-fastapi-app
```

### Remove Container

```bash
docker rm my-fastapi-app
```

## 🌐 VPS Deployment

### 1. Upload to VPS

Copy your project to VPS using SCP or SFTP:

```bash
scp -r app_to_deploy user@your-vps-ip:/home/user/
```

Or use Git:

```bash
# On VPS
git clone your-repo-url
cd app_to_deploy
```

### 2. Build and Run on VPS

SSH into your VPS:

```bash
ssh user@your-vps-ip
```

Navigate to project directory and build:

```bash
cd app_to_deploy
docker build -t fastapi-app .
docker run -d -p 8000:8000 --restart unless-stopped --name fastapi-app fastapi-app
```

### 3. Configure Firewall

Allow port 8000 (or use Nginx as reverse proxy on port 80/443):

```bash
# Ubuntu/Debian
sudo ufw allow 8000
```

### 4. Access Your Application

Open your browser and visit:
```
http://your-vps-ip:8000
```

## 🔄 Update Application

When you need to update:

```bash
# Stop and remove old container
docker stop fastapi-app
docker rm fastapi-app

# Rebuild image
docker build -t fastapi-app .

# Run new container
docker run -d -p 8000:8000 --restart unless-stopped --name fastapi-app fastapi-app
```

## 📊 Available Endpoints

### Web Interface
- `GET /` - SCADA Dashboard (main monitoring interface)
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)

### Machine Control API
- `GET /api/machine/status` - Get current machine status and all sensor readings
- `POST /api/machine/start` - Start the machine
- `POST /api/machine/stop` - Stop the machine
- `POST /api/machine/reset` - Reset production counters

### System API
- `GET /api/health` - Health check endpoint
- `GET /api/info` - System information

## 🎮 Using the SCADA Dashboard

1. **Start the Machine**: Click the "▶️ Start" button to begin operation
2. **Monitor Indicators**: Watch real-time updates of all sensors (updates every 2 seconds)
3. **Check Alarms**: System automatically triggers visual alarms when parameters exceed safe thresholds
4. **View Statistics**: Track production count, errors, uptime, and efficiency
5. **Stop the Machine**: Click "⏹️ Stop" to halt operations
6. **Reset Counters**: Click "🔄 Reset" to clear production statistics

## 📈 Sensor Parameters

| Parameter | Unit | Normal Range | Max Value | Alarm Threshold |
|-----------|------|--------------|-----------|-----------------|
| Motor Speed | RPM | 1200-1500 | 1500 | >90% |
| Temperature | °C | 60-80 | 95 | >90% |
| Pressure | bar | 3.5-5.0 | 6.5 | >90% |
| Vibration | mm/s | 0.5-1.5 | 3.0 | >85% |
| Power | kW | 70-100 | 120 | >90% |

## 🔧 Configuration

The application runs on port 8000 by default. To change the port, modify the Dockerfile or use:

```bash
docker run -d -p 3000:8000 --name fastapi-app fastapi-app
```

This maps port 3000 on the host to port 8000 in the container.

## 🛡️ Production Tips

1. **Use a reverse proxy (Nginx)**: Instead of exposing port 8000 directly, use Nginx on port 80/443
2. **SSL Certificate**: Use Let's Encrypt for HTTPS
3. **Auto-restart**: Use `--restart unless-stopped` flag
4. **Resource limits**: Use Docker resource constraints
5. **Logging**: Configure proper log management
6. **Monitoring**: Set up health check monitoring

## 📝 Example Nginx Configuration

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

## 📄 License

MIT License - feel free to use for any purpose.
