from accounts.views import CustomLoginView,RegisterView
from django.urls import path

urlpatterns = [
    path("register/",RegisterView.as_view(),name=""),
    path('login/', CustomLoginView.as_view(), name='custom-login'),
]