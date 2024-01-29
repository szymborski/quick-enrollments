from typing import List

from ninja import Schema


class CourseOut(Schema):
    id: int
    name: str
    max_students: int
    total_enrolled_students: int
    enrolled_students: List[str]

    @staticmethod
    def resolve_enrolled_students(obj) -> List[str]:
        return [enrollment.student_name for enrollment in obj.enrollments.all()]

    @staticmethod
    def resolve_total_enrolled_students(obj) -> int:
        return len(obj.enrollments.all())
