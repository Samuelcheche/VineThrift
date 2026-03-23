# Gmail SMTP Setup Guide for Vine Thrift

## Problem: Emails Not Sending

If you've configured SMTP but emails aren't being sent, the issue is almost always that **Gmail doesn't allow regular account passwords over SMTP**. You must use a Gmail App Password instead.

---

## Step-by-Step Gmail Configuration

### Step 1: Enable 2-Step Verification (if not already enabled)

1. Go to your Google Account: https://myaccount.google.com
2. Click **"Security"** in the left sidebar
3. Scroll down to **"2-Step Verification"**
4. Click **"Get started"** and follow the instructions
5. Verify your phone number and confirm

### Step 2: Generate an App Password

1. Go to **App passwords**: https://myaccount.google.com/apppasswords
   - If the option doesn't appear, make sure 2FA is enabled (Step 1)
   
2. Select:
   - **App**: Mail
   - **Device**: Windows Computer (or your device type)
   
3. Click **"Generate"**

4. Google will show you a **16-character password** like:
   ```
   abcd efgh ijkl mnop
   ```

5. **Copy this password** (without spaces)

---

## Step 3: Configure Vine Thrift

### Option A: Using .env File (RECOMMENDED)

1. Copy `.env.example` to `.env`:
   ```powershell
   Copy-Item .env.example .env
   ```

2. Open `.env` in a text editor and fill in your credentials:
   ```
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=true
   EMAIL_HOST_USER=Samuelonyango932@gmail.com
   EMAIL_HOST_PASSWORD=abcdefghijklmnop
   DEFAULT_FROM_EMAIL=Samuelonyango932@gmail.com
   SHOP_ADMIN_EMAIL=Samuelonyango932@gmail.com
   ```

3. Save the file (DO NOT commit to git - it's in .gitignore)

4. Run the server:
   ```powershell
   .\thrift\Scripts\python.exe manage.py runserver
   ```

---

### Option B: Using Environment Variables (PowerShell)

If you prefer not to use `.env`, set variables in PowerShell:

```powershell
$env:EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
$env:EMAIL_HOST = "smtp.gmail.com"
$env:EMAIL_PORT = "587"
$env:EMAIL_USE_TLS = "true"
$env:EMAIL_HOST_USER = "Samuelonyango932@gmail.com"
$env:EMAIL_HOST_PASSWORD = "abcdefghijklmnop"
$env:DEFAULT_FROM_EMAIL = "Samuelonyango932@gmail.com"
$env:SHOP_ADMIN_EMAIL = "Samuelonyango932@gmail.com"

.\thrift\Scripts\python.exe manage.py runserver
```

---

### Option C: Using Environment Variables (Command Prompt/Batch)

```batch
setx EMAIL_BACKEND django.core.mail.backends.smtp.EmailBackend
setx EMAIL_HOST smtp.gmail.com
setx EMAIL_PORT 587
setx EMAIL_USE_TLS true
setx EMAIL_HOST_USER Samuelonyango932@gmail.com
setx EMAIL_HOST_PASSWORD abcdefghijklmnop
setx DEFAULT_FROM_EMAIL Samuelonyango932@gmail.com
setx SHOP_ADMIN_EMAIL Samuelonyango932@gmail.com

python manage.py runserver
```

---

## Step 4: Test Email Sending

### Test 1: Send Test Email from Django Shell

```powershell
.\thrift\Scripts\python.exe manage.py shell
```

Then in the Python shell:

```python
from django.core.mail import send_mail
from django.conf import settings

result = send_mail(
    subject='Test Email from Vine Thrift',
    message='If you see this, SMTP is working!',
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=['Samuelonyango932@gmail.com'],
    fail_silently=False,
)

print(f"Email sent successfully: {result == 1}")
exit()
```

### Test 2: Use Contact Form

1. Start the server: `.\thrift\Scripts\python.exe manage.py runserver`
2. Go to: http://127.0.0.1:8000/contact/
3. Fill out the contact form and submit
4. Check both:
   - **Admin email** (Samuelonyango932@gmail.com) - should receive contact notification
   - **Your email** - should receive confirmation

---

## Troubleshooting

### Error: "Temporary server error"
- **Solution**: Check your App Password is exactly 16 characters (remove spaces)
- Regenerate a new App Password: https://myaccount.google.com/apppasswords

### Error: "Username and Password not accepted"
- **Solution**: You're using your regular Gmail password instead of an App Password
- Go to https://myaccount.google.com/apppasswords and create an App Password
- Make sure 2FA is enabled first

### Error: "Connection refused" or "timeout"
- **Solution**: Check EMAIL_HOST and EMAIL_PORT:
  - HOST: `smtp.gmail.com`
  - PORT: `587`
  - TLS: `true`

### Emails show in console but not actually sent
- **Solution**: Check EMAIL_BACKEND setting:
  - Development: `django.core.mail.backends.console.EmailBackend` (prints to terminal)
  - **Production**: `django.core.mail.backends.smtp.EmailBackend` (sends real emails)

### "Relay access denied"
- **Solution**: Your SMTP credentials are incorrect or EMAIL_HOST_USER is not set

---

## Gmail Security Warning

If you see a "Google couldn't verify this was you" message:

1. Go to: https://accounts.google.com/TexasHoldem
2. **Allow** the connection from your application
3. The app password will now work

---

## Alternative Email Providers

If Gmail SMTP isn't working, you can use:

### SendGrid
```
EMAIL_HOST = smtp.sendgrid.net
EMAIL_PORT = 587
EMAIL_HOST_USER = apikey
EMAIL_HOST_PASSWORD = your_sendgrid_api_key
```

### AWS SES
```
EMAIL_HOST = email-smtp.region.amazonaws.com
EMAIL_PORT = 587
EMAIL_HOST_USER = your_ses_username
EMAIL_HOST_PASSWORD = your_ses_password
```

### Mailgun
```
EMAIL_HOST = smtp.mailgun.org
EMAIL_PORT = 587
EMAIL_HOST_USER = your_mailgun_email@yourdomain
EMAIL_HOST_PASSWORD = your_mailgun_password
```

---

## .env File Security

**IMPORTANT**: The `.env` file contains sensitive credentials!

- Add to `.gitignore`: `echo ".env" >> .gitignore`
- Never commit `.env` to version control
- Use `.env.example` (without credentials) as a template for others
- On production, use environment variables or a secure vault service

---

## Contact & Support

If emails still don't work after following this guide:

1. Check Django logs for error messages
2. Verify EMAIL_BACKEND is set to `django.core.mail.backends.smtp.EmailBackend`
3. Test with Django shell (see Test 1 above)
4. Review your email provider's documentation

Good luck! 🚀
