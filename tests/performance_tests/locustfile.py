import random
from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    def on_start(self):
        "Send data test to Flask via an HTTP request"
        self.test_data = {
            "clubs": [
                {"name": "Club Test", "email": "test@example.com", "points": "10"}
            ],
            "competitions": [
                {
                    "name": "Competition Test",
                    "date": "2027-01-01 10:00:00",
                    "numberOfPlaces": "5",
                }
            ],
        }

        self.club_email = self.test_data["clubs"][0]["email"]
        self.club_name = self.test_data["clubs"][0]["name"]
        self.competition_name = self.test_data["competitions"][0]["name"]

        # Send data test to Flask
        self.client.post("/set-test-data", json=self.test_data)

    @task
    def index(self):
        self.client.get("/")

    @task
    def club_board(self):
        self.client.get("/club-board")

    @task
    def login(self):
        self.client.post("/login", {"email": self.club_email})

    @task
    def home(self):
        self.client.get("/home")

    @task
    def book(self):
        self.client.get(f"/book/{self.club_name}/{self.competition_name}")

    @task
    def purchase_places(self):
        places = random.randint(1, 5)
        self.client.post(
            "/purchase-places",
            {
                "club": self.club_name,
                "competition": self.competition_name,
                "places": str(places),
            },
        )

    @task
    def logout(self):
        self.client.get("/logout")
