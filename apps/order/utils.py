import logging
import requests
from math import ceil
from django.db.models import Sum, F

from django.conf import settings
from order.models import OrderItem, OrderStatus


logger = logging.getLogger(__name__)


def convert_json(response):
    try:
        return response.json()
    except Exception as e:
        logger.error("Error while converting Openroute Service response to json %s" % e)
        return None

def get_distance(order):
    """ return distance in km """
    api_key = settings.OPENROUTE_API_KEY
    print(api_key)

    restaurant_location = [order.restaurant.lat, order.restaurant.lon]
    client_location = [order.lat, order.lon]
    print([restaurant_location, client_location])

    if not all(restaurant_location + client_location):
        return 0

    error_msg = "Unknown Error"
    body = {"coordinates": [restaurant_location, client_location]}
    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        'Authorization': api_key,
        'Content-Type': 'application/json; charset=utf-8'
    }

    response = requests.post('https://api.openrouteservice.org/v2/directions/driving-car/json', json=body, headers=headers)
    response_json = convert_json(response)

    if response.status_code == 200 and response_json:
        summary = response_json.get('routes', [{}])[0].get('summary', {})
        distance = summary.get('distance', 0)
        return round(distance / 1000, 2)
    elif response.status_code in [401, 403] and response_json:
        error_msg = response_json.get('error', '')
    elif response.status_code in [400, 404] and response_json:
        error_msg = response_json.get('error', {}).get('message', '')

    logger.error(f"Openroute Service Error: {error_msg}", extra={
        'response_status': response.status_code,
        'response_content': response_json,
        'request_body': body
    })

    return 0


def get_delivery_time(instance):
    distance = get_distance(instance)
    total_count = OrderItem.objects.filter(
        order__status__in=[
            OrderStatus.WAITING, OrderStatus.CONFIRMED
        ]).aggregate(sum=Sum(F('count')))
    orders_count = total_count['sum'] if total_count['sum'] else 0
    print(total_count['sum'])
    print(distance)
    delivery_time = round(orders_count / 4, 2) * 5 + (3 * distance)
    delivery_time = ceil(delivery_time)
    if delivery_time > 60:
        return "%s:%s" % (delivery_time // 60, delivery_time % 60)
    return "%s" % delivery_time
