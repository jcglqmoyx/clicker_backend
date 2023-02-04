from django.urls import path

from authenticate.views import index

urlpatterns = [
    path('', index),
]
