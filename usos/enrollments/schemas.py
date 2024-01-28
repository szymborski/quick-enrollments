from ninja import Schema


class CourseEnrollmentIn(Schema):
    course_id: int
    student_name: str


class CourseEnrollmentOut(Schema):
    success: bool
