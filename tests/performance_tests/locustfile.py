import json
import random
from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    def on_start(self):
        with open("data/clubs.json", "r") as file:
            clubs_data = json.load(file)
            self.clubs = [club["name"] for club in clubs_data["clubs"]]
            self.emails = [club["email"] for club in clubs_data["clubs"]]

        with open("data/competitions.json", "r") as file:
            competitions_data = json.load(file)
            self.competitions = [
                comp["name"] for comp in competitions_data["competitions"]
            ]

        self.email = random.choice(self.emails)
        self.club = random.choice(self.clubs)
        self.competition = random.choice(self.competitions)

    @task
    def index(self):
        self.client.get("/")

    @task
    def club_board(self):
        self.client.get("/club-board")

    @task
    def login(self):
        self.client.post("/login", {"email": self.email})

    @task
    def home(self):
        self.client.get("/home")

    @task(4)
    def book(self):
        self.client.get(f"/book/{self.club}/{self.competition}")

    @task
    def purchase_places(self):
        places = random.randint(1, 5)
        self.client.post(
            "/purchase-places",
            {
                "club": self.club,
                "competition": self.competition,
                "places": str(places),
            },
        )

    @task
    def logout(self):
        self.client.get("/logout")
