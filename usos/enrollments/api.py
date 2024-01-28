from ninja import NinjaAPI

from enrollments.schemas import CourseEnrollmentOut, CourseEnrollmentIn
from enrollments.services import can_enroll, enroll_to_course

api = NinjaAPI(urls_namespace="enrollments")


@api.post("/enroll/", response=CourseEnrollmentOut)
async def enroll(request, input_data: CourseEnrollmentIn):
    is_valid = await can_enroll(input_data.course_id) 
    if is_valid:
        await enroll_to_course(input_data.course_id, input_data.student_name)
        return {"success": True}
    else:
        return {"success": False}
