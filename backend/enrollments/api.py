from django.conf import settings
from ninja import NinjaAPI
import redis.asyncio as redis

from enrollments.cache_services import can_enroll_cache, enroll_to_course_cache
from enrollments.schemas import CourseEnrollmentOut, CourseEnrollmentIn
from enrollments.services import can_enroll_db, enroll_to_course_db

api = NinjaAPI(urls_namespace="enrollments")


@api.post("/enroll/", response=CourseEnrollmentOut)
async def enroll(request, input_data: CourseEnrollmentIn):
    if await can_enroll_db(input_data.course_id):
        await enroll_to_course_db(input_data.course_id, input_data.student_name)
        success = True
    else:
        success = False
    return {"success": success}


@api.post("/enroll-cache/", response=CourseEnrollmentOut)
async def enroll_cache(request, input_data: CourseEnrollmentIn):
    redis_client = await redis.from_url(settings.CACHE_URL)

    course_id = input_data.course_id
    async with redis_client.lock(f"enroll_{course_id}"):
        if await can_enroll_cache(course_id):
            await enroll_to_course_cache(input_data.course_id, input_data.student_name)
            success = True
        else:
            success = False

        await redis_client.aclose()
        return {"success": success}
