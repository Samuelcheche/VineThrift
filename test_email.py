#!/usr/bin/env python
"""
Test script to verify Gmail SMTP configuration
Run: python test_email.py
"""

import os
import django
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Vinethrift.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_email_configuration():
    print("=" * 60)
    print("GMAIL SMTP CONFIGURATION TEST")
    print("=" * 60)
    
    print("\n📧 Current Email Settings:")
    print(f"  EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"  EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"  EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"  EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"  EMAIL_HOST_USER: {'*' * len(settings.EMAIL_HOST_USER) if settings.EMAIL_HOST_USER else 'NOT SET'}")
    print(f"  EMAIL_HOST_PASSWORD: {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 'NOT SET'}")
    print(f"  DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print(f"  SHOP_ADMIN_EMAIL: {settings.SHOP_ADMIN_EMAIL}")
    
    # Validation checks
    print("\n✓ Configuration Validation:")
    
    if not settings.EMAIL_HOST_USER:
        print("  ❌ ERROR: EMAIL_HOST_USER is not set!")
        print("     Set it in .env or as environment variable")
        return False
    else:
        print(f"  ✓ EMAIL_HOST_USER is set: {settings.EMAIL_HOST_USER}")
    
    if not settings.EMAIL_HOST_PASSWORD:
        print("  ❌ ERROR: EMAIL_HOST_PASSWORD is not set!")
        print("     Use a Gmail App Password (not your regular password)")
        return False
    else:
        print(f"  ✓ EMAIL_HOST_PASSWORD is set (length: {len(settings.EMAIL_HOST_PASSWORD)})")
    
    if settings.EMAIL_BACKEND == "django.core.mail.backends.console.EmailBackend":
        print("  ⚠️  WARNING: Using CONSOLE backend (emails print to terminal, not sent)")
        print("     Change EMAIL_BACKEND to: django.core.mail.backends.smtp.EmailBackend")
        return False
    else:
        print(f"  ✓ Using SMTP backend for real email sending")
    
    # Try to send test email
    print("\n📤 Attempting to send test email...")
    
    try:
        result = send_mail(
            subject="Test Email from Vine Thrift",
            message="If you received this, SMTP is working correctly!\n\n"
                   "Configuration is ready for production use.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.SHOP_ADMIN_EMAIL],
            fail_silently=False,
        )
        
        if result == 1:
            print("  ✅ SUCCESS! Email sent successfully!")
            print(f"     Sent to: {settings.SHOP_ADMIN_EMAIL}")
            print("\n🎉 Your SMTP configuration is working!")
            print("   Customers can now send contact forms and receive confirmations.")
            return True
        else:
            print("  ❌ Email function returned 0 (failed)")
            return False
            
    except Exception as e:
        print(f"  ❌ ERROR: {type(e).__name__}: {str(e)}")
        print("\nCommon issues:")
        print("  1. Check email address and app password are correct")
        print("  2. Make sure 2FA is enabled on Gmail account")
        print("  3. Verify EMAIL_HOST_PASSWORD is a 16-character App Password")
        print("  4. Check network connection and firewall (port 587)")
        return False

if __name__ == "__main__":
    success = test_email_configuration()
    print("\n" + "=" * 60)
    exit(0 if success else 1)
