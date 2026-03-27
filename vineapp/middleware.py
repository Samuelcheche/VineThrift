import threading

from django.core.management import call_command
from django.db import OperationalError


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
        except OperationalError as exc:
            message = str(exc).lower()
            if "no such table" not in message:
                raise

            if _migration_attempted:
                raise

            with _migration_lock:
                if not _migration_attempted:
                    call_command("migrate", interactive=False, run_syncdb=True, verbosity=0)
                    _migration_attempted = True

            # Retry request once after migration.
            return self.get_response(request)
