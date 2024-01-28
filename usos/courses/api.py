from typing import List

from ninja import NinjaAPI

from courses.models import Course
from courses.schemas import CourseOut

api = NinjaAPI(urls_namespace="courses")


@api.get("/", response=List[CourseOut])
async def courses(request):
    return [course async for course in Course.objects.prefetch_related("enrollments").all()]
