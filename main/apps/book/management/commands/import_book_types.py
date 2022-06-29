import yaml
from django.core.management.base import BaseCommand, CommandError

from ...models.book_type import BookType


class Command(BaseCommand):
    help = "Import book types from a yaml file"

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.HTTP_NOT_MODIFIED(
                "Import book types... wait...",
            )
        )
        BookType.objects.all().delete()
        try:
            with open(
                "main/apps/common/fixtures/book_types.yaml",
                "r",
            ) as yaml_file:
                data = yaml.safe_load(yaml_file)
                i = 0
                for item in data:
                    BookType.objects.create(
                        book_type=item["fields"]["book_type"],
                        book_id=item["fields"]["book"],
                        price=item["fields"]["price"],
                    )
                    i += 1
        except FileNotFoundError:
            raise CommandError("File book types yaml doesn't exists")

        self.stdout.write(
            self.style.SUCCESS(str(i) + " book types successfully imported")
        )
