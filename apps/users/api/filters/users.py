from django_filters.rest_framework import FilterSet, CharFilter
from django.db.models import Q

from user.models import User


class SearchUserFilterSet(FilterSet):
    full_name = CharFilter(method='get_full_name', distinct=True)

    class Meta:
        model = User
        fields = ('phone', 'country', 'state',)

    def get_full_name(self, queryset, name, value):
        return queryset.filter(first_name__istartswith=value)
