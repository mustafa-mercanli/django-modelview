from django.urls import path
from .views import ping,UsersView


urlpatterns = [
    path('ping', ping),
    path('users', UsersView.as_view()),
    path('users/<int:pk>', UsersView.as_view()),
]
