def get_max_students_count_key(course_id, add_prefix=False):
    key = f"course:{course_id}:max_students_count"
    if add_prefix:
        key = f":1:{key}"
    return key


def get_enrolled_students_count_key(course_id, add_prefix=False):
    key = f"course:{course_id}:enrolled_students_count"
    if add_prefix:
        key = f":1:{key}"
    return key


def get_enrolled_students_to_course_key(course_id, add_prefix=False):
    key = f"course:{course_id}:enrolled_students"
    if add_prefix:
        key = f":1:{key}"
    return key
