# Security Setup Guide

## Protecting Your API Keys

Your API keys should **never** be committed to version control or exposed in client-side code.

## Setup Instructions

### Step 1: Install python-dotenv

```bash
pip install python-dotenv
```

### Step 2: Create .env File

Copy the example file:
```bash
cp .env.example .env
```

Edit `.env` and add your actual API key:
```bash
GOOGLE_MAPS_API_KEY=AIzaSyC_your_actual_api_key_here
FLASK_SECRET_KEY=your_random_secret_key_here
```

### Step 3: Restrict Your API Key in Google Cloud

1. Go to https://console.cloud.google.com/apis/credentials
2. Click on your API key
3. **Application restrictions:**
   - Select "HTTP referrers (web sites)"
   - Add allowed referrers:
     - `http://localhost:*`
     - `http://127.0.0.1:*`
     - Your production domain (if deploying)
4. **API restrictions:**
   - Select "Restrict key"
   - Enable only: "Maps JavaScript API"
5. Click "Save"

### Step 4: Verify Setup

```bash
# Should show your API key (only you can see this)
cat .env

# Start the server
python app.py --port 8080

# Open browser to http://localhost:8080
# Map should load without errors
```

## How It Works

**Before (Insecure):**
```html
<!-- API key visible to anyone viewing page source -->
<script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY"></script>
```

**After (Secure):**
```javascript
// API key fetched from backend, not in HTML
fetch('/api/config')
  .then(config => loadGoogleMaps(config.google_maps_api_key))
```

The API key is:
- ✅ Stored in `.env` (excluded from git via `.gitignore`)
- ✅ Only loaded on the server
- ✅ Sent to client only when needed
- ✅ Still protected by HTTP referrer restrictions

## Additional Security Measures

### 1. Use HTTPS in Production

When deploying, always use HTTPS:
```python
# In production, set secure cookies
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
```

### 2. Add Rate Limiting

Install flask-limiter:
```bash
pip install flask-limiter
```

Add to `app.py`:
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/route', methods=['POST'])
@limiter.limit("10 per minute")
def find_route():
    # ... existing code
```

### 3. Add API Authentication (For Production)

For production deployment, add authentication:

```python
from functools import wraps
from flask import request

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key != os.getenv('API_SECRET_KEY'):
            return jsonify({"error": "Invalid API key"}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/route', methods=['POST'])
@require_api_key
def find_route():
    # ... existing code
```

### 4. Input Validation

Already implemented in the code, but always validate:
- Node IDs exist before routing
- Numeric values are in acceptable ranges
- String inputs are sanitized

### 5. CORS Configuration

For production, restrict CORS to specific domains:

```python
# Instead of CORS(app)
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://yourdomain.com"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})
```

## Deployment Checklist

Before deploying to production:

- [ ] Move API keys to environment variables
- [ ] Enable HTTPS
- [ ] Set up rate limiting
- [ ] Configure CORS properly
- [ ] Add API authentication
- [ ] Use a production WSGI server (gunicorn, waitress)
- [ ] Set `DEBUG=False`
- [ ] Review all error messages (don't expose internals)
- [ ] Enable logging
- [ ] Set up monitoring
- [ ] Back up data regularly

## Production WSGI Server

Don't use Flask's development server in production:

**Install gunicorn (Linux/Mac):**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8080 app:app
```

**Install waitress (Windows):**
```bash
pip install waitress
waitress-serve --host=0.0.0.0 --port=8080 app:app
```

## Environment Variables for Production

Add to `.env` for production:
```bash
# Google Maps
GOOGLE_MAPS_API_KEY=your_key

# Flask
FLASK_SECRET_KEY=generate_a_long_random_string
FLASK_ENV=production
DEBUG=False

# Server
HOST=0.0.0.0
PORT=8080

# Security
API_SECRET_KEY=another_random_string_for_api_auth

# Database (if using)
DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

## Generating Secure Keys

```python
# Generate a secure random key
import secrets
print(secrets.token_hex(32))
```

Or in bash:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## What NOT to Do

❌ Don't commit `.env` to git
❌ Don't hardcode API keys in code
❌ Don't share API keys in public forums
❌ Don't use the same key for dev and production
❌ Don't expose API keys in error messages
❌ Don't forget to rotate keys periodically

## What TO Do

✅ Use environment variables
✅ Add `.env` to `.gitignore`
✅ Restrict API keys in Google Cloud Console
✅ Use HTTPS in production
✅ Implement rate limiting
✅ Log security events
✅ Keep dependencies updated
✅ Review security regularly

## Monitoring API Usage

Check your Google Cloud Console regularly:
1. Go to "APIs & Services" → "Dashboard"
2. Select "Maps JavaScript API"
3. View usage charts
4. Set up billing alerts
5. Monitor for unusual activity

## If Your Key is Compromised

1. **Immediately** revoke the key in Google Cloud Console
2. Generate a new key
3. Update your `.env` file
4. Restart your application
5. Review logs for unauthorized usage
6. Report to Google if malicious usage occurred

## Questions?

- Check official Flask security docs: https://flask.palletsprojects.com/en/latest/security/
- Google Maps API security: https://developers.google.com/maps/api-security-best-practices
- OWASP security guidelines: https://owasp.org/www-project-web-security-testing-guide/
