from django.conf.urls import url
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from .views import get_addresses

router = DefaultRouter()
urlpatterns = router.urls
urlpatterns.append(url(r'insert-address', get_addresses))
