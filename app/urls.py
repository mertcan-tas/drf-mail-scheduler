from django.urls import path
from app.views import ScheduleMailView

urlpatterns = [
    path('schedule-mail/', ScheduleMailView.as_view(), name='schedule-mail'),
]