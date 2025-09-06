# Google Calendar Credentials Setup Guide

This guide walks you through setting up Google Calendar API credentials for the HR Agent system.

## 📋 Step-by-Step Setup

### 1. Access Google Cloud Console

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Sign in with your Google account

### 2. Create or Select a Project

**Option A: Create New Project**
1. Click the project dropdown at the top
2. Click "New Project"
3. Enter project name (e.g., "HR-Agent-Calendar")
4. Click "Create"

**Option B: Use Existing Project**
1. Click the project dropdown at the top
2. Select your existing project

### 3. Enable Google Calendar API

1. In the left sidebar, go to "APIs & Services" > "Library"
2. Search for "Google Calendar API"
3. Click on "Google Calendar API" from the results
4. Click "Enable"

### 4. Create OAuth 2.0 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - Choose "External" (unless you have a Google Workspace)
   - Fill in app name: "HR Agent Calendar Integration"
   - Add your email as developer contact
   - Click "Save and Continue" through the scopes and test users sections
4. For application type, select "Desktop application"
5. Enter name: "HR Agent Desktop Client"
6. Click "Create"

### 5. Download Credentials

1. After creation, you'll see a dialog with your client ID and secret
2. Click "Download JSON"
3. Save the file as `credentials.json` in your HR Agent project root directory

### 6. File Structure

Your project should now have:
```
HR_agent/
├── credentials.json          # ← Your downloaded file
├── google_calendar_mcp_config.py
├── google_calendar_mcp_tools.py
├── calendar_utils.py
├── requirements.txt
└── ... (other project files)
```

### 7. Test the Setup

Run the test command:
```bash
python google_calendar_scheduling_demo.py
```

On first run:
1. A browser window will open
2. Sign in to your Google account
3. Grant permissions to the HR Agent application
4. You'll see "The authentication flow has completed"
5. A `token.json` file will be created for future use

## 🔒 Security Best Practices

### Protect Your Credentials

1. **Never commit credentials to version control**
   ```bash
   echo "credentials.json" >> .gitignore
   echo "token.json" >> .gitignore
   ```

2. **Limit access to credential files**
   ```bash
   chmod 600 credentials.json
   chmod 600 token.json
   ```

3. **Use environment variables for production**
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
   ```

### OAuth Consent Screen Configuration

For production use, configure the OAuth consent screen properly:

1. **App Information**
   - App name: Your company's HR system name
   - User support email: Your support email
   - App logo: Optional company logo

2. **Authorized Domains**
   - Add your company domain
   - Add any domains where the app will be hosted

3. **Scopes**
   - `../auth/calendar` - Full calendar access
   - `../auth/calendar.events` - Event management

4. **Test Users** (during development)
   - Add email addresses of users who can test the integration

## 🔧 Troubleshooting

### Common Issues

**1. "Access denied" error**
```
Error: access_denied
```
- Ensure you granted all requested permissions
- Check that the Google account has calendar access
- Verify the OAuth consent screen is properly configured

**2. "Invalid client" error**
```
Error: invalid_client
```
- Ensure `credentials.json` is in the correct location
- Verify the file wasn't corrupted during download
- Check that you selected "Desktop application" as the type

**3. "Quota exceeded" error**
```
Error: quotaExceeded
```
- You've hit the Google Calendar API quota
- Wait for the quota to reset (usually daily)
- Consider requesting quota increase if needed regularly

**4. "Token refresh" errors**
```
Error: invalid_grant
```
- Delete `token.json` and re-authenticate
- Ensure system clock is accurate
- Check if the OAuth client is still active in Google Cloud Console

### Debug Steps

1. **Verify API is enabled**
   ```bash
   # Check if Calendar API is enabled in your project
   gcloud services list --enabled --filter="name:calendar"
   ```

2. **Test credentials manually**
   ```python
   from google_calendar_mcp_config import calendar_config
   print(calendar_config.test_connection())
   ```

3. **Check file permissions**
   ```bash
   ls -la credentials.json token.json
   ```

## 🌍 Production Considerations

### Multi-Environment Setup

**Development Environment**
- Use personal Google account
- Test with limited scope
- Keep credentials local

**Production Environment**
- Use service account (recommended)
- Implement proper secret management
- Set up monitoring and logging

### Service Account Setup (Advanced)

For production deployments, consider using service accounts:

1. In Google Cloud Console, go to "IAM & Admin" > "Service Accounts"
2. Create a new service account
3. Download the JSON key file
4. Enable domain-wide delegation (if needed)
5. Configure impersonation for calendar access

### Monitoring Setup

```python
import logging

# Set up logging for authentication events
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('calendar_auth.log'),
        logging.StreamHandler()
    ]
)
```

## 📞 Support Resources

- [Google Calendar API Documentation](https://developers.google.com/calendar/api)
- [OAuth 2.0 for Desktop Apps](https://developers.google.com/identity/protocols/oauth2/native-app)
- [Google Cloud Console](https://console.cloud.google.com/)
- [API Quotas and Limits](https://developers.google.com/calendar/api/guides/quota)

---

*This guide covers the essential setup steps. For advanced configurations or enterprise deployments, consult the Google Calendar API documentation.*
