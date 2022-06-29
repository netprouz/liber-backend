import yaml
from django.core.management.base import BaseCommand, CommandError

from ...models import Category


class Command(BaseCommand):
    help = "Import categories from a yaml file"

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.HTTP_NOT_MODIFIED(
                "Import categories... wait...",
            )
        )
        Category.objects.all().delete()
        try:
            with open(
                "main/apps/common/fixtures/categories.yaml",
                "r",
            ) as yaml_file:
                data = yaml.safe_load(yaml_file)
                i = 0
                for item in data:
                    Category.objects.create(
                        thumbnail=item["fields"]["thumbnail"],
                        title=item["fields"]["title"],
                        owner_id=item["fields"]["owner"],
                    )
                    i += 1
        except FileNotFoundError:
            raise CommandError("File categories yaml doesn't exists")

        self.stdout.write(
            self.style.SUCCESS(str(i) + " categories successfully imported")
        )
