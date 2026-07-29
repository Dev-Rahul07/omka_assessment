from django.urls import path
from .views import SubmissionListCreateView, SubmissionDetailView

urlpatterns = [
    path('submissions/', SubmissionListCreateView.as_view(), name='submission-list-create'),
    path('submissions/<int:pk>/', SubmissionDetailView.as_view(), name='submission-detail'),
]