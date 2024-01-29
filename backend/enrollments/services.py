import asyncio

from courses.models import Course
from enrollments.models import CourseEnrollment


async def can_enroll_db(course_id):
    course_future = Course.objects.only("max_students").aget(id=course_id)
    count_future = CourseEnrollment.objects.filter(course_id=course_id).acount()
    course, count = await asyncio.gather(course_future, count_future)

    return count < course.max_students


async def enroll_to_course_db(course_id, student_name):
    await CourseEnrollment.objects.acreate(
        course_id=course_id, student_name=student_name
    )
