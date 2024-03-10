# Django
from django.db.models import Q


def filter_data(request, query):
    # Initilize
    result = query
    # Get Q's
    search_by_name  = None if request.GET.get('byName', None) == "" else request.GET.get('byName', None)
    order_by_value  = None if request.GET.get('orderBy', None) == "" else request.GET.get('orderBy', None)
    order_direction = None if request.GET.get('orderDir', None) == "" else request.GET.get('orderDir', None)
    # Filter object name
    if search_by_name:
        by_name_q = Q(ar_name__icontains=search_by_name) | Q(fr_name__icontains=search_by_name) | Q(en_name__icontains=search_by_name)
        result = result.filter(by_name_q)
    # Order By Value
    if order_by_value:
        order_by_q = f"-{order_by_value}" if order_direction != "descending" else order_by_value
        result = result.order_by(order_by_q)

    return result