from rest_framework import generics

from ..common.permissions import CreatePermission, UpdateDeletePermission
from .models import Category, CategoryType
from .serializers import CategoryModelSerializer, CategoryListSerializer, CategoryUpdateSerializer
from rest_framework_simplejwt import authentication
from rest_framework import permissions


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    filterset_fields = ["title"]
    search_fields = ("title",)


category_list_api_view = CategoryListAPIView.as_view()


class CategoryCreateAPIView(generics.CreateAPIView):
    model = Category
    authentication_classes = [authentication.JWTAuthentication]
    serializer_class = CategoryModelSerializer
    permission_classes = [permissions.IsAuthenticated, CreatePermission]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


category_create_api_view = CategoryCreateAPIView.as_view()


class CategoryUpdateAPIView(generics.UpdateAPIView):
    queryset = Category.objects.all()
    authentication_classes = [authentication.JWTAuthentication]
    serializer_class = CategoryUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, UpdateDeletePermission]
    lookup_field = "guid"

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

category_update_api_view = CategoryUpdateAPIView.as_view()


class CategoryDeleteAPIView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    authentication_classes = [authentication.JWTAuthentication]
    serializer_class = CategoryModelSerializer
    permission_classes = [permissions.IsAuthenticated, UpdateDeletePermission]
    lookup_field = "guid"

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

category_delete_api_view = CategoryDeleteAPIView.as_view()
