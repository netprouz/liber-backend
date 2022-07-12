from django.db.models import Count, Sum, IntegerField, Q
from django.db.models.functions import Coalesce
from ..book.models.book_type import BookType, TYPEChoices
from ..category.models import Category
from ..order.models import Order
from ..account.models.user import User
from datetime import date
from datetime import timedelta

today = date.today()
week = today - timedelta(days=7)
month = today - timedelta(days=30)


def book_type_stats():
    result = {}
    base_query = BookType.objects.all()
    total_count = (base_query.aggregate(total_count=Count("*")))

    ONLINE = TYPEChoices.ONLINE
    AUDIO = TYPEChoices.AUDIO
    PAPER = TYPEChoices.PAPER

    online = stats_helper(base_query, ONLINE)
    audio = stats_helper(base_query, AUDIO)
    paper = stats_helper(base_query, PAPER)

    result['online'] = online
    result['audio'] = audio
    result['paper'] = paper
    result["total_count"] = total_count.get("total_count")

    return result


def category_stats():
    base_query = Category.objects.all()
    total_count = (base_query.aggregate(total_count=Count("*")))

    result = stats_helper(base_query)
    result["total_count"] = total_count.get("total_count")

    return result


def user_stats():
    base_query = User.objects.all()
    base_query = base_query.exclude(Q(is_staff=True) | Q(is_moderator=True) | Q(is_superuser=True))

    total_count = (base_query.aggregate(total_count=Count("*")))

    result = stats_helper(base_query)
    result["total_count"] = total_count.get("total_count")

    return result


def stats_helper(base_query, book_type=None):
    inner_result = {}

    if book_type is not None:
        base_query = base_query.filter(book_type=book_type)

    monthly = base_query.filter(created_at__date__gte=month)
    monthly = monthly.aggregate(count=Count('*'))
    inner_result["since_last_month"] = monthly.get("count", 0)

    weekly = base_query.filter(created_at__date__gte=week)
    weekly = weekly.aggregate(count=Count('*'))
    inner_result["since_last_week"] = weekly.get("count", 0)

    daily = base_query.filter(created_at__date__gte=today)
    daily = daily.aggregate(count=Count('*'))
    inner_result["today"] = daily.get("count", 0)

    return inner_result


def order_stats():
    base_query = Order.objects.all()

    result = {}

    daily = base_query.filter(created_at__date__gte=today)
    daily = daily.aggregate(count=Count('*'),
                            sum=Coalesce(Sum("total_price", output_field=IntegerField()), 0))
    result["today"] = dict(order_count=daily.get("count", 0),
                           order_amount=daily.get("sum"))

    weekly = base_query.filter(created_at__date__gte=week)
    weekly = weekly.aggregate(count=Count('*'),
                              sum=Coalesce(Sum("total_price", output_field=IntegerField()), 0))
    result["since_last_week"] = dict(order_count=weekly.get("count", 0),
                                     order_amount=weekly.get("sum"))

    monthly = base_query.filter(created_at__date__gte=month)
    monthly = monthly.aggregate(count=Count('*'),
                                sum=Coalesce(Sum("total_price", output_field=IntegerField()), 0))
    result["since_last_month"] = dict(order_count=monthly.get("count", 0),
                                      order_amount=monthly.get("sum"))

    monthly = base_query.aggregate(count=Count('*'),
                                   sum=Coalesce(Sum("total_price", output_field=IntegerField()), 0))
    result["total_orders"] = dict(order_count=monthly.get("count", 0),
                                  order_amount=monthly.get("sum"))

    return result
