from django.urls import path
from . import views

urlpatterns = [
    path('', views.ScheduleListView.as_view(), name='schedule_list'),
    path('group/<str:group_name>/', views.GroupScheduleView.as_view(), name='group_schedule'),
    path('teacher/<int:teacher_id>/', views.TeacherScheduleView.as_view(), name='teacher_schedule'),
    path('schedule/create/', views.ScheduleCreateView.as_view(), name='schedule_create'),
    path('schedule/<int:pk>/update/', views.ScheduleUpdateView.as_view(), name='schedule_update'),
    path('schedule/<int:pk>/delete/', views.ScheduleDeleteView.as_view(), name='schedule_delete'),
    path('classrooms/', views.classroom_availability, name='classroom_availability'),
    path('analysis/', views.analysis, name='analysis'),
] 