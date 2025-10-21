from locust import HttpUser, TaskSet, task
from core.environment.host import get_host_for_locust_testing


class NotepadBehavior(TaskSet):
    def on_start(self):
        self.index()

    @task(2)
    def index(self):
        response = self.client.get("/notepad")

        if response.status_code != 200:
            print(f"Notepad index failed: {response.status_code}")
        else:
            print("Notepad index succeeded")
            
    @task(1)
    def create_notepad(self):
        response = self.client.post(
            "/notepad/create",
            data={"title": "Locust Test Notepad", "body": "This is a test notepad created by Locust."},
        )

        if response.status_code != 200:
            print(f"Create notepad failed: {response.status_code}")
        else:
            print("Create notepad succeeded")

    @task(1)
    def get_notepad(self):
        response = self.client.get("/notepad/1")

        if response.status_code != 200:
            print(f"Get notepad failed: {response.status_code}")
        else:
            print("Get notepad succeeded")
            
            
    @task(1)
    def edit_notepad(self):
        response = self.client.post(
            "/notepad/edit/1",
            data={"title": "Updated Locust Test Notepad", "body": "This notepad has been updated by Locust."},
        )

        if response.status_code != 200:
            print(f"Edit notepad failed: {response.status_code}")
        else:
            print("Edit notepad succeeded")
            
    @task(1)
    def delete_notepad(self):
        response = self.client.post("/notepad/delete/1")

        if response.status_code != 200:
            print(f"Delete notepad failed: {response.status_code}")
        else:
            print("Delete notepad succeeded")


class NotepadUser(HttpUser):
    tasks = [NotepadBehavior]
    min_wait = 5000
    max_wait = 9000
    host = get_host_for_locust_testing()