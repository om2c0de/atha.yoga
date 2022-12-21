from django.contrib import admin

from .models import Course, Schedule, CourseComment, CourseReview


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "teacher",
        "course_type",
        "level",
        "complexity",
        "payment",
        "price",
        "single",
        "start_datetime",
        "deadline_datetime",
        "repeat_editing",
        "created_at",
    )
    list_display_links = ("id", "name")
    list_filter = (
        "course_type",
        "level",
        "complexity",
        "payment",
        "single",
        "start_datetime",
        "deadline_datetime",
        "repeat_editing",
        "created_at",
    )
    search_fields = ("name",)
    date_hierarchy = "created_at"


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "course",
        "start_at",
        "created_at",
    )
    list_filter = ("created_at",)
    date_hierarchy = "created_at"


@admin.register(CourseComment)
class CourseCommentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "course",
        "created_at",
    )
    search_fields = ("text",)
    list_filter = ("created_at",)
    date_hierarchy = "created_at"


@admin.register(CourseReview)
class CourseReviewAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "course",
        "star_rating",
        "created_at",
    )
    search_fields = ("text",)
    list_filter = ("star_rating", "created_at")
    date_hierarchy = "created_at"
