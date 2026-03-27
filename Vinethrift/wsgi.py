"""
WSGI config for Vinethrift project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Vinethrift.settings')


def _env_true(name, default=False):
	value = os.getenv(name)
	if value is None:
		return default
	return value.strip().lower() in {"1", "true", "yes", "on"}


def _run_startup_migrations():
	# Auto-migrate in Render (or when explicitly enabled) to avoid missing auth/session tables.
	render_env_detected = any(
		os.getenv(name)
		for name in ("RENDER", "RENDER_EXTERNAL_URL", "RENDER_EXTERNAL_HOSTNAME")
	)
	auto_migrate = _env_true("AUTO_MIGRATE", render_env_detected)
	if not auto_migrate:
		return

	try:
		call_command("migrate", interactive=False, run_syncdb=True, verbosity=1)
	except Exception as exc:
		# Don't block boot forever; keep the app up so logs/health checks are visible.
		print(f"Startup migration failed: {exc}")


_run_startup_migrations()

application = get_wsgi_application()
