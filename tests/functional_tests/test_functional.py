import pytest
import server
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time


URL = "http://127.0.0.1:5000"
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


def visit_homepage():
    driver.get(URL)


def navigate_to_club_board():
    link = driver.find_element(By.LINK_TEXT, "Club board")
    link.click()
    driver.back()


def login(email):
    email_field = driver.find_element(By.NAME, "email")
    email_field.send_keys(email)
    print("Email saisi:", email)
    form = driver.find_element(By.TAG_NAME, "form")
    form.submit()
    print("URL après connexion:", driver.current_url)


def book_places_for_competition():
    booking_link = driver.find_element(By.LINK_TEXT, "Book Places")
    booking_link.click()

    places_field = driver.find_element(By.NAME, "places")
    places_field.send_keys("3")
    time.sleep(2)
    form = driver.find_element(By.TAG_NAME, "form")
    form.submit()


def logout():
    logout_link = driver.find_element(By.LINK_TEXT, "Logout")
    logout_link.click()


@pytest.fixture
def setup(monkeypatch):
    fake_club = [{"name": "Club Test", "email": "test@example.com", "points": "10"}]
    fake_competition = [
        {
            "name": "Competition Test",
            "date": "2027-01-01 10:00:00",
            "numberOfPlaces": "5",
        }
    ]
    monkeypatch.setattr(server, "clubs", fake_club)
    monkeypatch.setattr(server, "competitions", fake_competition)


def test_run_functional():
    visit_homepage()
    navigate_to_club_board()
    login("test@example.com")
    print("Clubs mockés:", server.clubs)
    print("Comp mockés:", server.competitions)
    navigate_to_club_board()
    book_places_for_competition()
    logout()
