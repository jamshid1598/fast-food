from django.urls import path, include


app_name = 'fastfood'


urlpatterns = [
    path('api/', include("fastfood.api.urls", namespace="api")),
]
