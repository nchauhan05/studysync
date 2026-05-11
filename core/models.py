from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# ================= PROFILE =================

class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    field = models.CharField(max_length=100)

    interests = models.TextField(blank=True)

    goal = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


# ================= TASKS =================

class Task(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200)

    completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ================= SUBJECTS =================

class Subject(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ================= SAVED NOTES =================

class SavedNote(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200)

    note_link = models.URLField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ================= VIDEOS =================

class Video(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200)

    link = models.URLField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ================= CALENDAR NOTES =================

class CalendarNote(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    date = models.DateField()

    note = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"


# ================= STUDY TRACKER =================

class StudyTracker(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    hours = models.IntegerField(default=0)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.hours} hrs"


# ================= FOCUS SESSION =================

class FocusSession(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    minutes = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.minutes} mins"