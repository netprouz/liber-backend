import yaml
from django.core.management.base import BaseCommand, CommandError

from ...models.content import Content


class Command(BaseCommand):
    help = "Import book contents from a yaml file"

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.HTTP_NOT_MODIFIED(
                "Import book contents... wait...",
            )
        )
        Content.objects.all().delete()
        try:
            with open(
                "main/apps/common/fixtures/book_content.yaml",
                "r",
            ) as yaml_file:
                data = yaml.safe_load(yaml_file)
                i = 0
                for item in data:
                    Content.objects.create(
                        title=item["fields"]["title"],
                        book_type=item["fields"]["book_type"],
                        body=item["fields"]["body"],
                        book_id=item["fields"]["book"],
                        owner_id=item["fields"]["owner"],
                    )
                    i += 1
        except FileNotFoundError:
            raise CommandError("File book contents yaml doesn't exists")

        self.stdout.write(
            self.style.SUCCESS(str(i) + " book contents successfully imported")
        )
