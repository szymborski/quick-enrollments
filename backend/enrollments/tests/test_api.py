import pytest
from model_bakery import baker

from courses.models import Course
from enrollments.cache_keys import get_enrolled_students_count_key
from enrollments.models import CourseEnrollment
from django.core.cache import cache


@pytest.fixture
def enroll_url():
    return "/enrollments/enroll/"


@pytest.fixture
def cache_enroll_url():
    return "/enrollments/enroll-cache/"


def test_enroll_to_course(client, enroll_url):
    course = baker.make(Course, max_students=1)

    payload = {"course_id": course.id, "student_name": "John Doe"}
    response = client.post(enroll_url, payload, content_type="application/json")

    assert response.status_code == 200
    assert response.json() == {"success": True}
    assert CourseEnrollment.objects.count() == 1


def test_enroll_to_course_by_cache(client, cache_enroll_url):
    course = baker.make(Course, max_students=1)

    payload = {"course_id": course.id, "student_name": "John Doe"}
    response = client.post(cache_enroll_url, payload, content_type="application/json")

    assert response.status_code == 200
    assert response.json() == {"success": True}
    assert cache.get(get_enrolled_students_count_key(course.id)) == 1


def test_cant_enroll_to_course(client, enroll_url):
    course = baker.make(Course, max_students=1)
    baker.make("enrollments.CourseEnrollment", course=course)

    payload = {"course_id": course.id, "student_name": "John Doe"}
    response = client.post(enroll_url, payload, content_type="application/json")

    assert response.status_code == 200
    assert response.json() == {"success": False}
