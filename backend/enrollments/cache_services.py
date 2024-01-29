from django.conf import settings
from django.core.cache import cache
from django.db.models import Count
import redis.asyncio as redis
from redis import DataError

from courses.models import Course
from enrollments.cache_keys import (
    get_enrolled_students_count_key,
    get_enrolled_students_to_course_key,
    get_max_students_count_key,
)
from enrollments.models import CourseEnrollment


async def can_enroll_cache(course_id):
    count_key = get_enrolled_students_count_key(course_id)
    max_key = get_max_students_count_key(course_id)
    data = await cache.aget_many(
        [
            count_key,
            max_key,
        ]
    )
    try:
        enrolled_count = data[count_key]
        max_students = data[max_key]
    except KeyError:
        data = await sync_db_to_cache(course_id=course_id)
        enrolled_count = data[count_key]
        max_students = data[max_key]

    return enrolled_count < max_students


async def enroll_to_course_cache(course_id, student_name):
    r = await redis.from_url(settings.CACHE_URL)
    async with r.pipeline(transaction=True) as pipe:
        await (
            pipe.lpush(
                get_enrolled_students_to_course_key(course_id, add_prefix=True),
                student_name,
            )
            .incr(get_enrolled_students_count_key(course_id, add_prefix=True))
            .execute()
        )


async def sync_db_to_cache(course_id=None):
    courses = [
        course
        async for course in Course.objects.annotate(
            enrolled_students=Count("enrollments")
        ).all()
    ]
    if course_id:
        courses = [course for course in courses if course.id == course_id]

    to_set = {}
    for course in courses:
        to_set[get_enrolled_students_count_key(course.id)] = course.enrolled_students
        to_set[get_max_students_count_key(course.id)] = course.max_students

    if to_set:
        await cache.aset_many(to_set)

    return to_set


async def pop_student_from_course(client, course_id):
    key = get_enrolled_students_to_course_key(course_id, add_prefix=True)
    try:
        student = await client.rpop(key)
        return student.decode()
    except (AttributeError, DataError):
        return None


async def sync_cache_to_db():
    r = await redis.from_url(settings.CACHE_URL)

    courses = [course async for course in Course.objects.all()]

    to_create = []

    for course in courses:
        student = await pop_student_from_course(r, course.id)
        while student:
            to_create.append(
                CourseEnrollment(course_id=course.id, student_name=student)
            )
            student = await pop_student_from_course(r, course.id)

    if to_create:
        await CourseEnrollment.objects.abulk_create(to_create)
