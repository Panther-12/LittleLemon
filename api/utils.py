
from django.core.paginator import Paginator, EmptyPage

def calculate_total_cost(items):
    _sum = 0
    for item in items:
        _sum+=item['price']*int(item['quantity'])
    return _sum

def filter_data(request,unfiltered_data):
    items=unfiltered_data
    category_name = request.query_params.get('category')
    to_price = request.query_params.get('to_price')
    search = request.query_params.get('search')
    ordering = request.query_params.get('ordering')
    orders_delivery_delivered = request.query_params.get('orders_delivery_delivered')
    orders_delivery_pending = request.query_params.get('orders_delivery_pending')
    orders_delivery_customer_search = request.query_params.get('orders_delivery_customer_search')
    orders_manager_to_price = request.query_params.get('orders_manager_to_price')
    orders_manager_customer_search = request.query_params.get('orders_manager_customer_search')
    orders_customer_to_price = request.query_params.get('orders_customer_to_price')

    if category_name:
        items = unfiltered_data.filter(category__title=category_name)
    if to_price:
        items = unfiltered_data.filter(price__lte=to_price)
    if search:
        items = unfiltered_data.filter(name__icontains=search)
    if ordering:
        items = unfiltered_data.order_by(ordering)
    if orders_delivery_delivered:
        items = unfiltered_data.filter(delivered=orders_delivery_delivered)
    if orders_delivery_pending:
        items = unfiltered_data.filter(out_for_delivery=orders_delivery_pending)
    if orders_delivery_customer_search:
        items = unfiltered_data.filter(order__customer__username=orders_delivery_customer_search)
    if orders_manager_to_price:
        items = unfiltered_data.filter(amount__gte=orders_manager_to_price)
    if orders_manager_customer_search:
        items = unfiltered_data.filter(customer__username=orders_manager_customer_search)
    if orders_customer_to_price:
        items = unfiltered_data.filter(amount__gte=orders_customer_to_price)
    return items

def paginate_items(request,items):
    # pagination
    perpage = request.query_params.get('perpage', default=9)
    page = request.query_params.get('page', default=1)

    paginator = Paginator(items, perpage)
    try:
        items = paginator.page(number=page)
    except EmptyPage:
        items = []
    return items

def order_by_category(items):
    ordering_fields = ['category__title','name']
    items = items.order_by(*ordering_fields)
    return items