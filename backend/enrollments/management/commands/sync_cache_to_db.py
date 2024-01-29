import asyncio

from django.core.management.base import BaseCommand

from enrollments.cache_services import sync_cache_to_db


class Command(BaseCommand):
    help = "Description of your command"

    async def async_handle(self, *args, **options):
        await sync_cache_to_db()

    def handle(self, *args, **options):
        asyncio.run(self.async_handle(*args, **options))
