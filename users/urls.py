
from django.urls import path, include

from users.views import register_view

urlpatterns = [

    path('', include('django.contrib.auth.urls')),
    path('registration', register_view, name='registration')
]