from typing import List

from ninja import NinjaAPI

from courses.models import Course
from courses.schemas import CourseOut, CourseIn

api = NinjaAPI(urls_namespace="courses")


@api.get("/", response=List[CourseOut])
async def courses(request):
    return [
        course async for course in Course.objects.prefetch_related("enrollments").all()
    ]


@api.post("/")
async def add_course(request, course_data: CourseIn):
    await Course.objects.acreate(**course_data.dict())
    return True
