# from django.utils.translation import gettext_lazy as _

# from rest_framework.permissions import IsAuthenticated
# from rest_framework.generics import ListAPIView, RetrieveAPIView

# from drf_spectacular.utils import extend_schema

# from user.models import Notification
# from user.permissions import IsDriver
# from taxi.paginations import CustomPagination
# from user.api.filters.notification import NotificationFilter
# from user.api.serializers.notification import (
#     NotificationSerializer,
#     NotificationDetailSerializer,
# )


# @extend_schema(tags=['api.v1 user notifications (for client/driver)'])
# class NotificationList(ListAPIView):
#     """
#     get:
#         Returns a list of all notifications.
#     """

#     serializer_class = NotificationSerializer
#     permission_classes = [IsAuthenticated,]
#     pagination_class = CustomPagination

#     def get_queryset(self):
#         return Notification.objects.filter(
#             to_user=self.request.user,
#         ).values(
#             "id", "title", "image",
#         )


# @extend_schema(tags=['api.v1 user notifications (for client/driver)'])
# class UnReadNotificationList(ListAPIView):
#     """
#     get:
#         Returns a list of unread notifications.
#     """

#     serializer_class = NotificationSerializer
#     permission_classes = [IsAuthenticated,]
#     pagination_class = CustomPagination

#     def get_queryset(self):
#         return Notification.objects.filter(
#             to_user=self.request.user,
#             status=Notification.StatusChoices.WAITING
#         ).values(
#             "id", "title", "image",
#         )


# @extend_schema(tags=['api.v1 user notifications (for client/driver)'])
# class NotificationDetail(RetrieveAPIView):
#     """
#     parametrs: `pk`

#     GET request:
#         Returns user notification detail and updates notification `status`
#     """

#     queryset = Notification.objects.all()
#     serializer_class = NotificationDetailSerializer
#     permission_classes = [IsAuthenticated,]

#     def get_object(self):
#         obj = super(NotificationDetail, self).get_object()
#         obj.status = Notification.StatusChoices.READED
#         obj.save(update_fields=['status'])
#         return obj
