from django.contrib import admin
from .models import (
    Profile,
    Task,
    Subject,
    SavedNote,
    Video,
    CalendarNote,
    StudyTracker,
    FocusSession
)

# Register your models here

admin.site.register(Profile)
admin.site.register(Task)
admin.site.register(Subject)
admin.site.register(SavedNote)
admin.site.register(Video)
admin.site.register(CalendarNote)
admin.site.register(StudyTracker)
admin.site.register(FocusSession)