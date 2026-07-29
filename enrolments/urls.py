from django.urls import path
from .views import EnrolmentListCreateView, EnrolmentDetailView

urlpatterns = [
    path('enrolments/', EnrolmentListCreateView.as_view(), name='enrolment-list-create'),
    path('enrolments/<int:pk>/', EnrolmentDetailView.as_view(), name='enrolment-detail'),
]