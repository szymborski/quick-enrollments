from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 2.5)

    @task
    def enroll_course_1(self):
        self.client.post("/enrollments/enroll-cache/", json={"course_id": 1, "student_name": "John"})

    @task
    def enroll_course_2(self):
        self.client.post("/enrollments/enroll-cache/", json={"course_id": 2, "student_name": "Mat"})
