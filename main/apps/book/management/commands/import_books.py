from urllib.request import urlopen
import yaml
from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from ...models.book import Book


class Command(BaseCommand):
    help = "Import books from a yaml file"

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.HTTP_NOT_MODIFIED(
                "Import books... wait...",
            )
        )
        Book.objects.all().delete()
        try:
            with open(
                "main/apps/common/fixtures/books.yaml",
                "r",
            ) as yaml_file:
                data = yaml.safe_load(yaml_file)
                i = 0
                for item in data:
                    # https://stackoverflow.com/questions/64263748/how-download-image-from-url-to-django
                    thumbnail_tmp = NamedTemporaryFile(delete=True)
                    response = urlopen(item["fields"]["thumbnail"])
                    thumbnail_tmp.write(response.read())
                    thumbnail_tmp.flush()
                    Book.objects.create(
                        title=item["fields"]["title"],
                        author=item["fields"]["author"],
                        thumbnail=File(thumbnail_tmp),
                        category_id=item["fields"]["category"],
                        language=item["fields"]["language"],
                        hardcover=item["fields"]["hardcover"],
                        short_description=item["fields"]["short_description"],
                        published_date=item["fields"]["published_date"],
                        owner_id=item["fields"]["owner"],
                    )
                    i += 1
        except FileNotFoundError:
            raise CommandError("File books yaml doesn't exists")

        self.stdout.write(
            self.style.SUCCESS(
                str(i) + " books successfully imported",
            )
        )
