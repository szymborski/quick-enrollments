import pytest
from model_bakery import baker

from courses.models import Course
from enrollments.models import CourseEnrollment


@pytest.fixture
def enroll_url():
    return "/enrollments/enroll/"


def test_enroll_to_course(client, enroll_url, django_assert_max_num_queries):
    course = baker.make(Course, max_students=1)
    
    payload = {
        "course_id": course.id,
        "student_name": "John Doe"
    }
    response = client.post(enroll_url, payload, content_type='application/json')
    print(response)
    assert response.status_code == 200
    assert response.json() == {"success": True}
    assert CourseEnrollment.objects.count() == 1


def test_cant_enroll_to_course(client, enroll_url, django_assert_max_num_queries):
    course = baker.make(Course, max_students=1)
    baker.make("enrollments.CourseEnrollment", course=course)

    payload = {
        "course_id": course.id,
        "student_name": "John Doe"
    }
    response = client.post(enroll_url, payload, content_type='application/json')

    assert response.status_code == 200
    assert response.json() == {"success": False}
