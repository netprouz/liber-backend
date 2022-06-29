import yaml
from django.core.management.base import BaseCommand, CommandError

from ...models.review import Review


class Command(BaseCommand):
    help = "Import book reviews from a yaml file"

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.HTTP_NOT_MODIFIED(
                "Import book reviews... wait...",
            )
        )
        Review.objects.all().delete()
        try:
            with open(
                "main/apps/common/fixtures/book_reviews.yaml",
                "r",
            ) as yaml_file:
                data = yaml.safe_load(yaml_file)
                i = 0
                for item in data:
                    Review.objects.create(
                        title=item["fields"]["title"],
                        book_id=item["fields"]["book"],
                        owner_id=item["fields"]["owner"],
                    )
                    i += 1
        except FileNotFoundError:
            raise CommandError("File book reviews yaml doesn't exists")

        self.stdout.write(
            self.style.SUCCESS(str(i) + " book reviews successfully imported")
        )
