
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import MovieViewSet, RatingViewSet

router = routers.DefaultRouter()  # allows us to have the standard rest routing urls (put, post, get, delete)
router.register('movies', MovieViewSet)
router.register('ratings', RatingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
