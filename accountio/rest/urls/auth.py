from django.urls import path, include
from accountio.rest.views.auth import UserLoginView

urlpatterns = [
    path("/user", UserLoginView.as_view(), name="login-user"),
]
