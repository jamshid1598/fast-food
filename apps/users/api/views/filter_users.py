from django.conf import settings
from django.db.models import Count, F, Q
from drf_yasg.utils import swagger_auto_schema

from rest_framework.generics import (
    ListAPIView, CreateAPIView, UpdateAPIView,
    DestroyAPIView, ListCreateAPIView, RetrieveAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from user.models import User, Gender
from core.models import Reaction, REACTION
from core.api.serializers.reaction import (
    ReactionSerializer, LikeSerializer, MyLikeSerializer,
)
from user.api.serializers.filter_users import FilterUsersSerializer
from user.api.pagination import RandomUserPagination, LikesPagination, SearchUserPagination
from user.api.filters.users import SearchUserFilterSet


class FilterUsersAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FilterUsersSerializer
    pagination_class = RandomUserPagination
    user_filters = None

    def get_queryset(self):
        curr_user = self.request.user
        filters = self.user_filters

        gender = Gender.opposite_one(curr_user.gender)
        excludes = {"id": curr_user.id}

        if 'gender' not in filters and gender:
            filters['gender'] = gender
            excludes['gender'] = curr_user.gender
        orderings = {"country__in": filters.pop('country__in', [curr_user.country])}

        if 'hobbies__in' in filters:
            orderings["hobbies__in"] = filters.pop('hobbies__in', list(curr_user.hobbies.values_list('id', flat=True)))
        qs = User.objects.filter_randomly(filters=filters, excludes=excludes, orderings=orderings, user=curr_user)

        return qs.distinct().annotate(
            likes=Count(F('reactions'), distinct=True, filter=Q(reactions__reaction=REACTION.LIKED)),
        )

    def get_serializer_context(self, *args, **kwargs):
        context = super().get_serializer_context(*args, **kwargs)
        if self.user_filters:
            context['user_filters'] = {
                "age_from": self.user_filters['_age__gte'] if '_age__gte' in self.user_filters else settings.MIN_AGE_LIMIT,
                "age_till": self.user_filters['_age__lte'] if '_age__lte' in self.user_filters else 60,
                "gender": self.user_filters.get('gender')
            }

        return context

    @swagger_auto_schema(tags=('api.v1 filter-users', ))
    def get(self, request, *args, **kwargs):
        try:
            self.user_filters = request.user.filter_options.filters()
        except User.filter_options.RelatedObjectDoesNotExist:
            self.user_filters = {}
        return self.list(request, *args, **kwargs)


class FilterUserAPI(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FilterUsersSerializer
    pagination_class = RandomUserPagination
    filterset_fields = ['pk']
    user_filters = {}

    def get_queryset(self):
        if self.request.query_params.get('pk') is None:
            raise NotFound('userIDNeeded', 404)
        else:
            filters = {"pk": self.request.query_params.get('pk')}

        qs = User.objects.filter_randomly(filters=filters, excludes={}, orderings={}, user=self.request.user)
        return qs.annotate(
            likes=Count(F('reactions'), filter=Q(reactions__reaction=REACTION.LIKED))).distinct()

    def filter_queryset(self, queryset):
        return queryset

    def get_object(self):
        try:
            obj = self.get_queryset()[0]
            return obj
        except Exception:
            raise NotFound('userNotFound', 404)

    @swagger_auto_schema(tags=('api.v1 filter-users', ))
    def get(self, request, *args, **kwargs):
        try:
            self.user_filters = request.user.filter_options.filters()
        except User.filter_options.RelatedObjectDoesNotExist:
            self.user_filters = {}
        return self.retrieve(request, *args, **kwargs)

    def get_serializer_context(self, *args, **kwargs):
        context = super().get_serializer_context(*args, **kwargs)
        if self.user_filters:
            context['user_filters'] = {
                "age_from": self.user_filters['_age__gte'] if '_age__gte' in self.user_filters else settings.MIN_AGE_LIMIT,
                "age_till": self.user_filters['_age__lte'] if '_age__lte' in self.user_filters else 60,
                "gender": self.user_filters.get('gender')
            }

        return context


class ReactionAPI(CreateAPIView):
    serializer_class = ReactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Reaction.objects.filter(created_by=self.request.user).select_related('user')
        return qs

    @swagger_auto_schema(tags=('api.v1 filter-users', ))
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def partial_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ReactionEditDeleteAPI(UpdateAPIView, DestroyAPIView):
    serializer_class = ReactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reaction.objects.filter(created_by=self.request.user).select_related('user')

    @swagger_auto_schema(tags=('api.v1 filter-users', ))
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    @swagger_auto_schema(tags=('api.v1 filter-users', ))
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class MyLikesAPI(ListCreateAPIView):
    queryset = Reaction.objects.filter(reaction=REACTION.LIKED)
    serializer_class = MyLikeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)

    @swagger_auto_schema(tags=('api.v1 filter-users', ))
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(tags=('api.v1 filter-users', ))
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user, reaction=REACTION.LIKED
        )


class LikesAPI(ListAPIView):
    queryset = Reaction.objects.filter(reaction=REACTION.LIKED)
    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = LikesPagination

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @swagger_auto_schema(tags=('api.v1 filter-users', ))
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class MyBlocksAPI(ListCreateAPIView):
    queryset = Reaction.objects.filter(reaction=REACTION.BLOCKED)
    serializer_class = MyLikeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)

    @swagger_auto_schema(tags=('api.v1 filter-users', ))
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(tags=('api.v1 filter-users', ))
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user, reaction=REACTION.BLOCKED
        )


class SearchUserAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FilterUsersSerializer
    pagination_class = SearchUserPagination
    filterset_class = SearchUserFilterSet
    user_filters = {}

    def get_queryset(self):
        return User.objects.all()

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset).distinct()
        queryset = queryset.select_related(
            'main_image', 'country', 'state'
        ).prefetch_related('hobbies', 'created_profileimages').annotate(
            likes=Count(F('reactions'), filter=Q(reactions__reaction=REACTION.LIKED)))
        return queryset

    @swagger_auto_schema(tags=('api.v1 filter-users',))
    def get(self, request, *args, **kwargs):
        try:
            self.user_filters = request.user.filter_options.filters()
        except User.filter_options.RelatedObjectDoesNotExist:
            self.user_filters = {}
        return self.list(request, *args, **kwargs)

    def get_serializer_context(self, *args, **kwargs):
        context = super().get_serializer_context(*args, **kwargs)
        if self.user_filters:
            context['user_filters'] = {
                "age_from": self.user_filters['_age__gte'] if '_age__gte' in self.user_filters else settings.MIN_AGE_LIMIT,
                "age_till": self.user_filters['_age__lte'] if '_age__lte' in self.user_filters else 60,
                "gender": self.user_filters.get('gender')
            }

        return context
