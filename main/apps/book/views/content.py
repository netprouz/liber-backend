from rest_framework import generics

from ...common.permissions import CreatePermission, UpdateDeletePermission
from ..models.content import Content
from ..serializers.content import (
    ContentCreateUpdateSerializer,
    ContentDetailSerializer,
    ContentListSerializer,
)


class ContentCreateAPIView(generics.CreateAPIView):
    model = Content
    serializer_class = ContentCreateUpdateSerializer
    permission_classes = [CreatePermission]

    def perform_create(self, serializer):
        return self.model.objects.create_content_instance(
            self.request.user,
            serializer.validated_data,
        )


content_create_api_view = ContentCreateAPIView.as_view()


class ContentListAPIView(generics.ListAPIView):
    queryset = Content.objects.values("guid", "title", "book_type")
    serializer_class = ContentListSerializer
    filterset_fields = ["title", "book_type", "book__guid"]
    search_fields = ["title"]


content_list_api_view = ContentListAPIView.as_view()


class ContentDetailAPIView(generics.RetrieveAPIView):
    queryset = Content.objects.get_content_detail()
    serializer_class = ContentDetailSerializer
    lookup_field = "guid"


content_detail_api_view = ContentDetailAPIView.as_view()


class ContentUpdateAPIView(generics.UpdateAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentCreateUpdateSerializer
    permission_classes = [UpdateDeletePermission]
    lookup_field = "guid"

    def perform_update(self, serializer):
        serializer.instance.update_content(serializer.validated_data)


content_update_api_view = ContentUpdateAPIView.as_view()


class ContentDeleteAPIView(generics.DestroyAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentListSerializer
    permission_classes = [UpdateDeletePermission]
    lookup_field = "guid"


content_delete_api_view = ContentDeleteAPIView.as_view()
