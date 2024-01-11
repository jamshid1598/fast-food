from django.urls import path
from fastfood.api.views.restaurant import (
    RestaurantList, RestaurantCreate,
    RestaurantDetail, RestaurantUpdate, RestaurantDelete
)


app_name = 'api'


urlpatterns = [
    path("restaurants/list/", RestaurantList.as_view(), name='restaurants_list'),
    path("restaurants/create/", RestaurantCreate.as_view(), name='restaurants_create'),
    path("restaurants/detail/<int:pk>/", RestaurantDetail.as_view(), name='restaurants_detail'),
    path("restaurants/update/<int:pk>/", RestaurantUpdate.as_view(), name='restaurants_update'),
    path("restaurants/delete/<int:pk>/", RestaurantDelete.as_view(), name='restaurants_delete'),
]
