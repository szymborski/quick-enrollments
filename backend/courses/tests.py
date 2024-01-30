import pytest
from model_bakery import baker

from courses.models import Course


@pytest.fixture
def list_url():
    return "/courses/"


def test_courses_list(client, list_url, django_assert_max_num_queries):
    courses = baker.make(Course, _quantity=20)
    for course in courses:
        baker.make("enrollments.CourseEnrollment", course=course, _quantity=2)

    with django_assert_max_num_queries(19):
        response = client.get(list_url)
        assert response.status_code == 200
        assert len(response.json()[0]["enrolled_students"]) == 2


async def test_add_course(async_client, list_url):
    payload = {
        "name": "Test Course",
        "max_students": 2,
    }
    response = await async_client.post(list_url, payload, content_type="application/json")

    assert response.status_code == 200
    assert await Course.objects.aget()
