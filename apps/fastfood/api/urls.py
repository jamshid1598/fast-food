from django.urls import path
from fastfood.api.views.restaurant import (
    RestaurantList, RestaurantCreate,
    RestaurantDetail, RestaurantUpdate, RestaurantDelete
)
from fastfood.api.views.fastfood import (
    FastFoodList, FastFoodCreate,
    FastFoodDetail, FastFoodUpdate, FastFoodDelete
)


app_name = 'api'


urlpatterns = [
    path("restaurants-list/", RestaurantList.as_view(), name='restaurants_list'),
    path("restaurants-create/", RestaurantCreate.as_view(), name='restaurants_create'),
    path("restaurants-detail/<int:pk>/", RestaurantDetail.as_view(), name='restaurants_detail'),
    path("restaurants-update/<int:pk>/", RestaurantUpdate.as_view(), name='restaurants_update'),
    path("restaurants-delete/<int:pk>/", RestaurantDelete.as_view(), name='restaurants_delete'),

    path("fastfood-list/", FastFoodList.as_view(), name='fastfood_list'),
    path("fastfood-create/", FastFoodCreate.as_view(), name='fastfood_create'),
    path("fastfood-detail/<int:pk>/", FastFoodDetail.as_view(), name='fastfood_detail'),
    path("fastfood-update/<int:pk>/", FastFoodUpdate.as_view(), name='fastfood_update'),
    path("fastfood-delete/<int:pk>/", FastFoodDelete.as_view(), name='fastfood_delete'),
]
