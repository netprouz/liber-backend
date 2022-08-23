import yaml
from django.core.management.base import BaseCommand, CommandError

from ...models.user import User


class Command(BaseCommand):
    help = "Import users from a yaml file"

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.HTTP_NOT_MODIFIED(
                "Import users... wait...",
            )
        )
        User.objects.all().delete()
        try:
            with open(
                "main/apps/common/fixtures/users.yaml",
                "r",
            ) as yaml_file:
                data = yaml.safe_load(yaml_file)
                i = 0
                for item in data:
                    user_obj = User.objects.create_user(
                        phone_number=item["fields"]["username"],
                        first_name=item["fields"]["first_name"],
                        profile_picture=item["fields"]["profile_picture"],
                        # last_name=item["fields"]["last_name"],
                        # email=item["fields"]["email"],
                        gender=item["fields"]["gender"],
                        date_of_birth=item["fields"]["date_of_birth"],
                        date_joined=item["fields"]["date_joined"],
                        is_staff=item["fields"]["is_staff"],
                        is_active=item["fields"]["is_active"],
                        is_moderator=item["fields"]["is_moderator"],
                        is_superuser=item["fields"]["is_superuser"],
                    )
                    user_obj.set_password(item["fields"]["password"])
                    i += 1
        except FileNotFoundError:
            raise CommandError("File users yaml doesn't exists")

        self.stdout.write(
            self.style.SUCCESS(
                str(i) + " users successfully imported",
            )
        )
