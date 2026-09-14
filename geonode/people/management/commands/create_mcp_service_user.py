import os

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create and maintain the dedicated read-only MCP service user."

    def handle(self, *args, **options):
        username = os.getenv("MCP_SERVICE_USERNAME", "mcp_service").strip()
        password = os.getenv("MCP_SERVICE_PASSWORD", "")
        email = os.getenv("MCP_SERVICE_EMAIL", "mcp-service@localhost").strip()

        if not password:
            self.stdout.write(
                self.style.WARNING(
                    "MCP_SERVICE_PASSWORD is not set; skipping MCP service user creation."
                )
            )
            return

        if len(password) < 12:
            raise CommandError("MCP_SERVICE_PASSWORD must contain at least 12 characters")

        if not username:
            raise CommandError("MCP_SERVICE_USERNAME must not be empty")

        user_model = get_user_model()
        user, created = user_model.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "is_active": True,
                "is_staff": False,
                "is_superuser": False,
            },
        )

        if user.is_staff or user.is_superuser:
            raise CommandError(
                f"Refusing to use privileged existing account {username!r} as the MCP service user"
            )

        if created:
            user.set_password(password)
            user.save(update_fields=["password"])

        # GeoNode normally adds new users to contributors. Remove inherited
        # groups and direct permissions so this dedicated account stays read-only.
        user.groups.clear()
        user.user_permissions.clear()
        read_permissions = Permission.objects.filter(
            content_type__app_label="base",
            codename__in=("view_resourcebase", "download_resourcebase"),
        )
        user.user_permissions.add(*read_permissions)

        self.stdout.write(
            self.style.SUCCESS(
                f"MCP service user {username!r} {'created' if created else 'verified'} as read-only"
            )
        )
