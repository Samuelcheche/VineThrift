import threading
import os

from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.db import DatabaseError, OperationalError, ProgrammingError


_migration_lock = threading.Lock()
_migration_attempted = False


class AutoMigrateOnMissingTableMiddleware:
    """Run migrations once if a request fails due to missing sqlite tables."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        global _migration_attempted

        try:
            return self.get_response(request)
        except (OperationalError, ProgrammingError, DatabaseError) as exc:
            message = str(exc).lower()
            recoverable_markers = (
                "no such table",
                "no such column",
                "auth_user",
                "django_session",
            )
            if not any(marker in message for marker in recoverable_markers):
                raise

            if _migration_attempted:
                raise

            with _migration_lock:
                if not _migration_attempted:
                    call_command("migrate", interactive=False, run_syncdb=True, verbosity=0)
                    _ensure_superuser_from_env()
                    _migration_attempted = True

            # Retry request once after migration.
            return self.get_response(request)


def _ensure_superuser_from_env():
    username = os.getenv("DJANGO_SUPERUSER_USERNAME")
    password = os.getenv("DJANGO_SUPERUSER_PASSWORD")
    email = os.getenv("DJANGO_SUPERUSER_EMAIL", "")

    if not username or not password:
        return

    user_model = get_user_model()
    user, created = user_model.objects.get_or_create(username=username, defaults={"email": email})

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

    if created:
        user.save()
    else:
        user.save(update_fields=list(dict.fromkeys(updates)))
