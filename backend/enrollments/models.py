from django.db import models


class CourseEnrollment(models.Model):
    course = models.ForeignKey(
        "courses.Course", on_delete=models.CASCADE, related_name="enrollments"
    )
    student_name = models.TextField()
