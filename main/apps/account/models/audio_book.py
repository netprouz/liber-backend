from ..managers.audio_book import AudionBookManager
from .user_book import UserBook


class AudioBook(UserBook):
    objects = AudionBookManager()

    class Meta:
        proxy = True
        ordering = ("-id",)
        verbose_name = "Audio Book"
        verbose_name_plural = "Audio Books"

    def __str__(self) -> str:
        return f"{self.guid}"
