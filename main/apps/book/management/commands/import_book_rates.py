import yaml
from django.core.management.base import BaseCommand, CommandError

from ...models.rate import Rate


class Command(BaseCommand):
    help = "Import rates from a yaml file"

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.HTTP_NOT_MODIFIED(
                "Import rates... wait...",
            )
        )
        Rate.objects.all().delete()
        try:
            with open(
                "main/apps/common/fixtures/book_rates.yaml",
                "r",
            ) as yaml_file:
                data = yaml.safe_load(yaml_file)
                i = 0
                for item in data:
                    Rate.objects.create(
                        point=item["fields"]["point"],
                        book_id=item["fields"]["book"],
                        owner_id=item["fields"]["owner"],
                    )
                    i += 1
        except FileNotFoundError:
            raise CommandError("File rates yaml doesn't exists")

        self.stdout.write(
            self.style.SUCCESS(
                str(i) + " rates successfully imported",
            )
        )
