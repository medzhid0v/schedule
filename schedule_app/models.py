from django.db import models

# Create your models here.

class Teacher(models.Model):
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    middle_name = models.CharField('Отчество', max_length=100, blank=True)
    email = models.EmailField('Email', unique=True)
    
    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

class Group(models.Model):
    name = models.CharField('Название группы', max_length=50, unique=True)
    course = models.IntegerField('Курс')
    faculty = models.CharField('Факультет', max_length=100)
    
    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ['course', 'name']
    
    def __str__(self):
        return self.name

class Classroom(models.Model):
    number = models.CharField('Номер аудитории', max_length=20, unique=True)
    capacity = models.IntegerField('Вместимость')
    building = models.CharField('Корпус', max_length=50)
    
    class Meta:
        verbose_name = 'Аудитория'
        verbose_name_plural = 'Аудитории'
        ordering = ['building', 'number']
    
    def __str__(self):
        return f"{self.building}-{self.number}"

class Subject(models.Model):
    name = models.CharField('Название предмета', max_length=200)
    code = models.CharField('Код предмета', max_length=20, unique=True)
    
    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Schedule(models.Model):
    DAYS_OF_WEEK = [
        ('MON', 'Понедельник'),
        ('TUE', 'Вторник'),
        ('WED', 'Среда'),
        ('THU', 'Четверг'),
        ('FRI', 'Пятница'),
        ('SAT', 'Суббота'),
    ]
    
    TIMESLOTS = [
        ('1', '8:30-10:00'),
        ('2', '10:10-11:40'),
        ('3', '12:00-13:30'),
        ('4', '13:40-15:10'),
        ('5', '15:20-16:50'),
        ('6', '17:00-18:30'),
    ]
    
    day_of_week = models.CharField('День недели', max_length=3, choices=DAYS_OF_WEEK)
    timeslot = models.CharField('Время', max_length=1, choices=TIMESLOTS)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='Предмет')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='Преподаватель')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Группа')
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, verbose_name='Аудитория')
    week_type = models.CharField('Тип недели', max_length=1, choices=[('1', 'Нечетная'), ('2', 'Четная')], default='1')
    
    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписание'
        unique_together = ['day_of_week', 'timeslot', 'group', 'week_type']
        ordering = ['day_of_week', 'timeslot']
    
    def __str__(self):
        return f"{self.get_day_of_week_display()} {self.get_timeslot_display()} - {self.subject} ({self.group})"
