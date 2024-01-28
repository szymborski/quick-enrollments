from django.db import models


class Course(models.Model):
    name = models.TextField()
    max_students = models.PositiveIntegerField()
