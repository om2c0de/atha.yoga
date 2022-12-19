from django.core.validators import MinValueValidator
from django.db import models

from core.models import User, TimeStampedModel


class LessonTypes(models.TextChoices):
    ONLINE = "ONLINE"
    VIDEO = "VIDEO"


class LessonLevels(models.TextChoices):
    STARTING = "STARTING"
    CONTINUER = "CONTINUER"
    ADVANCED = "ADVANCED"


class LessonPaymentTypes(models.TextChoices):
    PAYMENT = "PAYMENT"
    DONATION = "DONATION"
    FREE = "FREE"


class LessonComplexities(models.TextChoices):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"


class RepetitionWeekdays(models.TextChoices):
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"


class Lesson(TimeStampedModel):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    lesson_type = models.CharField(max_length=30, choices=LessonTypes.choices)
    level = models.CharField(max_length=30, choices=LessonLevels.choices)
    single = models.BooleanField(default=False)
    duration = models.DurationField()
    start_datetime = models.DateTimeField()
    deadline_datetime = models.DateTimeField(null=True)
    complexity = models.CharField(max_length=30, choices=LessonComplexities.choices)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    link = models.URLField()
    link_info = models.CharField(max_length=100, blank=True)
    repeat_editing = models.BooleanField(default=False)
    payment = models.CharField(max_length=30, choices=LessonPaymentTypes.choices)
    price = models.FloatField(validators=(MinValueValidator(limit_value=0),))

    favorites = models.ManyToManyField(
        User, related_name="favorite_lessons", blank=True
    )

    class Meta:
        verbose_name = "Занятие"
        verbose_name_plural = "Занятия"


class Schedule(TimeStampedModel):
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="schedules"
    )
    weekday = models.CharField(max_length=40, choices=RepetitionWeekdays.choices)
    start_time = models.TimeField()
    participants = models.ManyToManyField(User)

    class Meta:
        verbose_name = "Расписание"
        verbose_name_plural = "Расписания"


class Comment(TimeStampedModel):
    text = models.TextField(max_length=512)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    lesson = models.ForeignKey(
        Lesson, related_name="comments", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


class Ticket(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    amount = models.CharField(max_length=8)

    class Meta:
        verbose_name = "Билет"
        verbose_name_plural = "Билеты"
