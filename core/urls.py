from django.conf.urls import include
from django.urls import path

from core.router import router

urlpatterns = [path("", include(router.urls))]
