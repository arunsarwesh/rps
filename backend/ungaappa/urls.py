from django.urls import path
from .views import HandGestureRecognitionView

urlpatterns = [
    path("recognize/", HandGestureRecognitionView.as_view(), name="recognize"),
]
