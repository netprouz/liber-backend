from rest_framework import generics

from ...common.permissions import DeletePersonalObjectPermission
from ..models.audio_book import AudioBook
from ..serializers import audio_book


class AudioBookListAPIView(generics.ListAPIView):
    queryset = AudioBook.objects.filter_with_rates()
    serializer_class = audio_book.AudioBookSerializer

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


audio_book_list_api_view = AudioBookListAPIView.as_view()


class AudioBookDetailAPIView(generics.RetrieveAPIView):
    queryset = AudioBook.objects.all()
    serializer_class = audio_book.AudioBookDetailSerializer
    permission_classes = [DeletePersonalObjectPermission, ]
    lookup_field = "guid"


audio_book_detail_api_view = AudioBookDetailAPIView.as_view()


class AudioBookDeleteAPIView(generics.DestroyAPIView):
    queryset = AudioBook.objects.all()
    serializer_class = audio_book.AudioBookDetailSerializer
    permission_classes = [DeletePersonalObjectPermission, ]
    lookup_field = "guid"


audio_book_delete_api_view = AudioBookDeleteAPIView.as_view()
