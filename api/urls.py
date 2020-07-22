
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()  # allows us to have the standard rest routing urls (put, post, get, delete)

urlpatterns = [
    path('', include(router.urls)),
]
