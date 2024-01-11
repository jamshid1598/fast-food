from django_filters.rest_framework import FilterSet

from user.models import User


class UserFilter(FilterSet):

    class Meta:
        model = User
        fields = {
            'first_name': ['istartswith'],
            'last_name': ['istartswith'],
            'id': ['exact'],
            'country': ['exact'],
            'state': ['exact'],
            'hobbies': ['exact'],
            'gender': ['exact'],
            'created_at': ['date__gte', 'date__lte'],
            '_age': ['gte', 'lte'],
        }
