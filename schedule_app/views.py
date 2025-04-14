from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Count, Q
from .models import Schedule, Group, Teacher, Classroom, Subject

# Create your views here.

class ScheduleListView(ListView):
    model = Schedule
    template_name = 'schedule_app/schedule_list.html'
    context_object_name = 'schedules'
    
    def get_queryset(self):
        queryset = Schedule.objects.all()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(subject__name__icontains=search_query) |
                Q(teacher__last_name__icontains=search_query) |
                Q(group__name__icontains=search_query)
            )
        return queryset

class GroupScheduleView(ListView):
    model = Schedule
    template_name = 'schedule_app/group_schedule.html'
    context_object_name = 'schedules'

    def get_queryset(self):
        group = get_object_or_404(Group, name=self.kwargs['group_name'])
        return Schedule.objects.filter(group=group)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group_name'] = self.kwargs['group_name']
        return context

class TeacherScheduleView(ListView):
    model = Schedule
    template_name = 'schedule_app/teacher_schedule.html'
    context_object_name = 'schedules'

    def get_queryset(self):
        teacher = get_object_or_404(Teacher, id=self.kwargs['teacher_id'])
        return Schedule.objects.filter(teacher=teacher)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teacher'] = get_object_or_404(Teacher, id=self.kwargs['teacher_id'])
        return context

class ScheduleCreateView(CreateView):
    model = Schedule
    template_name = 'schedule_app/schedule_form.html'
    fields = ['day_of_week', 'timeslot', 'subject', 'teacher', 'group', 'classroom', 'week_type']
    success_url = reverse_lazy('schedule_list')

class ScheduleUpdateView(UpdateView):
    model = Schedule
    template_name = 'schedule_app/schedule_form.html'
    fields = ['day_of_week', 'timeslot', 'subject', 'teacher', 'group', 'classroom', 'week_type']
    success_url = reverse_lazy('schedule_list')

class ScheduleDeleteView(DeleteView):
    model = Schedule
    template_name = 'schedule_app/schedule_confirm_delete.html'
    success_url = reverse_lazy('schedule_list')

def classroom_availability(request):
    classrooms = Classroom.objects.all()
    schedules = Schedule.objects.all()
    context = {
        'classrooms': classrooms,
        'schedules': schedules,
    }
    return render(request, 'schedule_app/classroom_availability.html', context)

def analysis(request):
    # Анализ загруженности групп
    group_load = Group.objects.annotate(
        total_classes=Count('schedule')
    ).order_by('-total_classes')

    # Анализ загруженности преподавателей
    teacher_load = Teacher.objects.annotate(
        total_classes=Count('schedule')
    ).order_by('-total_classes')

    # Анализ использования аудиторий
    classroom_usage = Classroom.objects.annotate(
        total_classes=Count('schedule')
    ).order_by('-total_classes')

    # Поиск свободных аудиторий
    all_timeslots = Schedule.TIMESLOTS
    all_days = Schedule.DAYS_OF_WEEK
    all_week_types = [('1', 'Нечетная'), ('2', 'Четная')]
    
    free_classrooms = []
    for classroom in Classroom.objects.all():
        for day in all_days:
            for timeslot in all_timeslots:
                for week_type in all_week_types:
                    if not Schedule.objects.filter(
                        classroom=classroom,
                        day_of_week=day[0],
                        timeslot=timeslot[0],
                        week_type=week_type[0]
                    ).exists():
                        free_classrooms.append({
                            'classroom': classroom,
                            'day': day[1],
                            'time': timeslot[1],
                            'week_type': week_type[1]
                        })

    context = {
        'group_load': group_load,
        'teacher_load': teacher_load,
        'classroom_usage': classroom_usage,
        'free_classrooms': free_classrooms,
    }
    return render(request, 'schedule_app/analysis.html', context)
