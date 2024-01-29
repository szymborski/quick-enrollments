from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 2.5)

    @task
    def enroll_course(self):
        self.client.post("/enrollments/enroll/", json={"course_id": 1, "student_name": "John"})
