from asgiref.sync import sync_to_async
from model_bakery import baker
from django.core.cache import cache

from courses.models import Course
from enrollments.cache_keys import (
    get_max_students_count_key,
    get_enrolled_students_count_key,
)
from enrollments.cache_services import (
    sync_db_to_cache,
    enroll_to_course_cache,
    sync_cache_to_db,
)
from enrollments.models import CourseEnrollment


async def test_db_to_redis():
    course = await sync_to_async(baker.make)(Course, max_students=31)
    await sync_to_async(baker.make)(CourseEnrollment, course=course, _quantity=2)

    await sync_db_to_cache()

    max_students_key = get_max_students_count_key(course.id)
    enrolled_students_key = get_enrolled_students_count_key(course.id)

    assert await cache.aget(max_students_key) == 31
    assert await cache.aget(enrolled_students_key) == 2


async def test_sync_cache_to_db():
    course = await sync_to_async(baker.make)(Course, max_students=31)

    assert await CourseEnrollment.objects.acount() == 0
    await enroll_to_course_cache(course.id, "John Doe")
    await enroll_to_course_cache(course.id, "Mark Twain")

    assert cache.get(get_enrolled_students_count_key(course.id)) == 2

    await sync_cache_to_db()

    students = {
        enrollment.student_name async for enrollment in CourseEnrollment.objects.all()
    }

    assert students == {"John Doe", "Mark Twain"}
