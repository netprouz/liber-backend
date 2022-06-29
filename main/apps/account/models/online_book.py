from ..managers.online_book import OnlineBookManager
from .user_book import UserBook


class OnlineBook(UserBook):
    objects = OnlineBookManager()

    class Meta:
        proxy = True
        ordering = ("-id",)
        verbose_name = "Online Book"
        verbose_name_plural = "Online Books"

    def __str__(self) -> str:
        return f"{self.guid}"
