from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from . import api


class BookTypeAPIView(APIView):

    def get(self, request):
        book_type_results = api.book_type_stats()

        return Response(book_type_results, status=status.HTTP_200_OK)


book_type_statistics_api_view = BookTypeAPIView.as_view()


class CategoryStatsAPIView(APIView):

    def get(self, request):
        category_results = api.category_stats()

        return Response(category_results, status=status.HTTP_200_OK)


category_statistics_api_view = CategoryStatsAPIView.as_view()


class OrderStatsAPIView(APIView):

    def get(self, request):
        order_stats_result = api.order_stats()

        return Response(order_stats_result, status=status.HTTP_200_OK)


order_statistics_api_view = OrderStatsAPIView.as_view()


class UserStatsAPIView(APIView):

    def get(self, request):
        user_stats = api.user_stats()

        return Response(user_stats, status=status.HTTP_200_OK)


user_statistics_api_view = UserStatsAPIView.as_view()