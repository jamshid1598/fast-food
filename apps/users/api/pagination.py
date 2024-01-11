from collections import OrderedDict

from django.core.paginator import InvalidPage
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class RandomUserPagination(PageNumberPagination):
    page_size = 10


class SearchUserPagination(PageNumberPagination):
    page_size = 20


class LikesPagination(PageNumberPagination):
    page_size = 20

    def paginate_queryset(self, queryset, request, view=None):
        self.unseen_likes = queryset.filter(seen=False).count()
        if self.unseen_likes and self.unseen_likes > self.page_size:
            self.page_size = self.unseen_likes
        data = super().paginate_queryset(queryset.order_by('seen', '-id'), request, view=None)
        if self.unseen_likes:
            queryset.filter(seen=False).update(seen=True)

        return data

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data),
            ('page_count', self.unseen_likes)
        ]))


class UsersPaginationForAdmin(PageNumberPagination):
    page_size = 15


class BlockedEmailPagination(PageNumberPagination):
    page_size = 100
