from django.contrib import admin
from django.urls import path, include
from stonksapp.urls import urlpatterns as stonksapp_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(stonksapp_urls)),
]
