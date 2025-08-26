# 🚨 Emergency Email Alert System Setup Guide

This guide will help you set up the email notification system that automatically sends alerts to counselors and parents when the EQ bot detects high emotional distress.

## 📋 Prerequisites

1. **Python 3.8+** installed on your system
2. **A Gmail account** (or other SMTP email provider)
3. **App Password** from Gmail (not your regular password)

## 🔧 Setup Steps

### Step 1: Configure Email Settings

1. **Create App Password for Gmail:**
   - Go to [Google Account Settings](https://myaccount.google.com/)
   - Navigate to **Security** → **2-Step Verification** → **App passwords**
   - Generate a new app password for "BrightSide"
   - Copy the 16-character password (it will look like: `abcd efgh ijkl mnop`)

2. **Update the `.env` file:**
   ```bash
   cd python_backend
   cp .env.example .env
   ```
   
   Edit `.env` with your actual email credentials:
   ```bash
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your_actual_email@gmail.com
   SMTP_PASSWORD=your_16_character_app_password_here
   DEFAULT_FROM=your_actual_email@gmail.com
   
   # API Configuration
   PORT=8000
   
   # Security Configuration
   EMERGENCY_ALERT_ENABLED=true
   MAX_ALERTS_PER_HOUR=5
   ```

### Step 2: Install Python Dependencies

```bash
cd python_backend
pip install -r requirements.txt
```

### Step 3: Test the Email Configuration

1. **Update test contacts** in `test_emergency_system.py`:
   ```python
   # Replace these with real email addresses for testing
   "email": "counselor@example.com",  # Your test email
   "email": "parent@example.com",     # Another test email
   ```

2. **Run the test:**
   ```bash
   python test_emergency_system.py
   ```

### Step 4: Start the Backend Server

```bash
python start_server.py
```

The server will start on `http://localhost:8000`

### Step 5: Test the Full System

1. **Start the React frontend** (in main project directory):
   ```bash
   npm run dev
   ```

2. **Navigate to the EQ Bot** page in your browser

3. **Trigger a high distress alert** by typing messages like:
   - "I feel completely overwhelmed and hopeless"
   - "I don't know what to do anymore, everything feels impossible"
   - "I'm feeling extremely depressed and can't cope"

4. **Check the console logs** to see if the alert was sent

5. **Check the email inbox** of your test contacts

## 🎯 How It Works

### Distress Detection
- The EQ bot analyzes user messages for emotional content
- When distress score exceeds **70/100** (configurable), an alert is triggered
- Only **one alert per session** is sent to prevent spam

### Alert Priority
- **Counselors and parents** are contacted first (highest priority)
- **Friends** can be added to the notification list if needed
- **Rate limiting** prevents more than 5 alerts per hour per user

### Email Content
- **Professional, urgent formatting** with clear severity levels
- **Actionable recommendations** for the recipients
- **Crisis resources** included in every alert
- **User's recent message** included for context

## 🔍 Troubleshooting

### Common Issues

1. **"SMTP Authentication failed"**
   - Ensure you're using an App Password, not your regular Gmail password
   - Double-check the username and password in `.env`

2. **"Cannot connect to API server"**
   - Make sure the Python backend is running: `python start_server.py`
   - Check that port 8000 is not blocked

3. **"No emergency contacts found"**
   - Ensure user profiles have contacts with valid email addresses
   - Check that contact relationships are set to 'counselor' or 'parent'

4. **Emails not being sent**
   - Check the `email_service.log` file for detailed error messages
   - Verify SMTP settings in `.env`
   - Test with `test_emergency_system.py`

### Debug Steps

1. **Check server logs:**
   ```bash
   cd python_backend
   tail -f email_service.log
   ```

2. **Test individual components:**
   ```bash
   # Test API health
   curl http://localhost:8000/api/health
   
   # Test emergency notification
   python test_emergency_system.py
   ```

3. **Enable debug mode:**
   Add to `.env`:
   ```
   LOG_LEVEL=DEBUG
   ```

## 🛡️ Security Features

- **Rate limiting**: Maximum 5 alerts per user per hour
- **Environment variables**: Sensitive data stored securely
- **Input validation**: All data validated before processing
- **Error handling**: Graceful failure without exposing sensitive info

## 📧 Email Providers

While this guide uses Gmail, you can configure other providers:

### Outlook/Hotmail
```bash
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
```

### Yahoo Mail
```bash
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
```

### Custom SMTP
```bash
SMTP_SERVER=your-smtp-server.com
SMTP_PORT=587  # or 465 for SSL
```

## 🚀 Production Deployment

For production use:

1. **Use a dedicated email service** (SendGrid, Mailgun, etc.)
2. **Set up proper logging** and monitoring
3. **Use a database** for rate limiting instead of in-memory storage
4. **Configure proper CORS** settings
5. **Use HTTPS** for all API calls
6. **Set up backup notification methods** (SMS, push notifications)

## 📝 Testing Checklist

- [ ] Email credentials configured correctly
- [ ] Python backend server starts without errors
- [ ] Health check endpoint responds
- [ ] Test emergency notification sends emails
- [ ] Frontend EQ bot triggers alerts on high distress
- [ ] Rate limiting works (try sending multiple alerts)
- [ ] Email formatting looks professional
- [ ] Log files show detailed information

## 💡 Tips

- **Test with real email addresses** during development
- **Keep the distress threshold configurable** for different users
- **Monitor email delivery rates** in production
- **Provide feedback to users** when alerts are sent
- **Include unsubscribe options** in production emails
- **Set up email templates** for different severity levels

---

🆘 **Need Help?** Check the `email_service.log` file for detailed error messages, or contact the development team.
