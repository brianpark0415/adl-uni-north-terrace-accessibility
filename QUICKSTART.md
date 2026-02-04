# Quick Start Guide

## Starting the Server

### Default (Port 5000)
```bash
python app.py
```
Then open: http://localhost:5000

### If Port 5000 is Busy (Use Port 8080)
```bash
python app.py --port 8080
```
Then open: http://localhost:8080

### Custom Port
```bash
python app.py --port 3000
```
Then open: http://localhost:3000

## Common Issues

### "Address already in use" on macOS
Port 5000 is used by AirPlay Receiver. Either:

**Option 1:** Use a different port
```bash
python app.py --port 8080
```

**Option 2:** Disable AirPlay Receiver
1. System Settings → General → AirDrop & Handoff
2. Turn off "AirPlay Receiver"

**Option 3:** Kill the process
```bash
lsof -ti:5000 | xargs kill -9
```

### "Port already in use" on Windows/Linux
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID [PID_NUMBER] /F

# Linux
lsof -ti:5000 | xargs kill -9
```

## Running the Demo (No Server Needed)

If you just want to test the routing algorithm without the web interface:
```bash
python demo.py
```

This works without needing any port and demonstrates all the routing features.

## Recommended Workflow

1. **First time:** Run `python check_setup.py` to verify installation
2. **Test routing:** Run `python demo.py` to see the algorithm work
3. **Start web app:** Run `python app.py --port 8080`
4. **Open browser:** Go to http://localhost:8080
5. **Add Google Maps API key** to `templates/index.html` (line with `YOUR_API_KEY`)

## Getting a Google Maps API Key

1. Go to https://console.cloud.google.com/
2. Create a new project (or select existing)
3. Enable "Maps JavaScript API"
4. Create credentials → API Key
5. Copy the key
6. Edit `templates/index.html`
7. Find: `src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&callback=initMap"`
8. Replace `YOUR_API_KEY` with your actual key

## Without Google Maps

The system works fine without Google Maps - you'll just see a basic map placeholder. All the routing functionality still works through the API.

## Available Commands

```bash
# Check setup
python check_setup.py

# Run demo
python demo.py

# Start server (default port 5000)
python app.py

# Start server (custom port)
python app.py --port 8080

# Start server (custom host and port)
python app.py --host 127.0.0.1 --port 3000
```

## Testing the API

Once the server is running, test the API:

```bash
# Get all nodes
curl http://localhost:8080/api/nodes

# Get statistics
curl http://localhost:8080/api/statistics

# Find a route
curl -X POST http://localhost:8080/api/route \
  -H "Content-Type: application/json" \
  -d '{"start": "hub_central", "end": "bs_main_entrance", "preference": "balanced"}'
```

## Next Steps

1. ✅ Verify installation: `python check_setup.py`
2. ✅ Test routing: `python demo.py`
3. ✅ Start server: `python app.py --port 8080`
4. 🔧 Add Google Maps API key (optional)
5. 📍 Add more campus locations (see DATA_COLLECTION_GUIDE.md)
6. 🚀 Implement enhancements (see README.md)
