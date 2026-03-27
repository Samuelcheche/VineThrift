import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Vinethrift.settings")

import django


django.setup()

from django.contrib.auth import get_user_model  # noqa: E402


def env_bool(name, default=False):
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


if not env_bool("AUTO_CREATE_SUPERUSER", True):
    raise SystemExit(0)

username = os.getenv("DJANGO_SUPERUSER_USERNAME")
email = os.getenv("DJANGO_SUPERUSER_EMAIL", "")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

if not username or not password:
    raise SystemExit(0)

User = get_user_model()
user, created = User.objects.get_or_create(username=username, defaults={"email": email})

if created:
    user.is_staff = True
    user.is_superuser = True
    user.set_password(password)
    user.save(update_fields=["is_staff", "is_superuser", "password", "email"])
    print(f"Created superuser: {username}")
else:
    updates = []
    if not user.is_staff:
        user.is_staff = True
        updates.append("is_staff")
    if not user.is_superuser:
        user.is_superuser = True
        updates.append("is_superuser")
    if email and user.email != email:
        user.email = email
        updates.append("email")

    user.set_password(password)
    updates.append("password")

    user.save(update_fields=list(dict.fromkeys(updates)))
    print(f"Updated superuser: {username}")
