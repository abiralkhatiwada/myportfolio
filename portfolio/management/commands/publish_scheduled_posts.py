from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from portfolio.models import BlogPost


class Command(BaseCommand):
    help = "Publish approved blog posts whose scheduled time has arrived."

    def handle(self, *args, **options):
        now = timezone.now()

        with transaction.atomic():
            # Materialize the queryset once so select_for_update() locks rows
            # before running count() and update().
            posts = list(
                BlogPost.objects.select_for_update().filter(
                    status="scheduled",
                    is_published=False,
                    scheduled_at__lte=now,
                )
            )
            count = len(posts)

            if count == 0:
                self.stdout.write(
                    self.style.WARNING(
                        "No scheduled articles are ready for publication."
                    )
                )
                return

            post_ids = [post.pk for post in posts]
            BlogPost.objects.filter(pk__in=post_ids).update(
                status="published",
                is_published=True,
                published_at=now,  # Optional: include if your model tracks this
            )

        self.stdout.write(
            self.style.SUCCESS(f"Successfully published {count} article(s).")
        )