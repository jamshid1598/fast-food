from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from apps.users.views import change_language
from config.swaggers import urlpatterns as swagger_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('change-language/', change_language, name='change_language'),
    path('users/', include('users.urls', namespace='users')),
    path("", include('fastfood.urls', namespace='fastfood')),
    path("order/", include('order.urls', namespace='order')),
    *swagger_urls,
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
