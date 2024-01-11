from django.urls import path, include


app_name = 'users'


urlpatterns = [
    path('api/', include("user.api.urls.urls", namespace="api")),
]
