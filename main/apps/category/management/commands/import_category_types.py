import yaml
from django.core.management.base import BaseCommand, CommandError

from ...models import CategoryType


class Command(BaseCommand):
    help = "Import category types from a yaml file"

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.HTTP_NOT_MODIFIED(
                "Import category types... wait...",
            )
        )
        CategoryType.objects.all().delete()
        try:
            with open(
                "main/apps/common/fixtures/category_types.yaml",
                "r",
            ) as yaml_file:
                data = yaml.safe_load(yaml_file)
                i = 0
                for item in data:
                    CategoryType.objects.create(
                        price=item["fields"]["price"],
                        category_id=item["fields"]["category"],
                        days=item["fields"]["days"],
                    )
                    i += 1
        except FileNotFoundError:
            raise CommandError("File category types yaml doesn't exists")

        self.stdout.write(
            self.style.SUCCESS(
                str(i) + " category types successfully imported",
            )
        )
