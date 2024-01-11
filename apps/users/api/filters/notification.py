from django_filters.rest_framework import FilterSet
from user.models import Notification


class NotificationFilter(FilterSet):

    class Meta:
        model = Notification
        fields = ('status',)
