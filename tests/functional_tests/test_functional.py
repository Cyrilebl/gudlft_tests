import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


URL = "http://127.0.0.1:5000"
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


def inject_test_data():
    """Send data to Flask server"""
    test_data = {
        "clubs": [{"name": "Club Test", "email": "test@example.com", "points": "10"}],
        "competitions": [
            {
                "name": "Competition Test",
                "date": "2027-01-01 10:00:00",
                "numberOfPlaces": "5",
            }
        ],
    }
    response = requests.post(f"{URL}/set-test-data", json=test_data)


def visit_homepage():
    driver.get(URL)


def navigate_to_club_board():
    link = driver.find_element(By.LINK_TEXT, "Club board")
    link.click()
    driver.back()


def login(email):
    email_field = driver.find_element(By.NAME, "email")
    email_field.send_keys(email)
    form = driver.find_element(By.TAG_NAME, "form")
    form.submit()


def book_places_for_competition():
    booking_link = driver.find_element(By.LINK_TEXT, "Book Places")
    booking_link.click()
    places_field = driver.find_element(By.NAME, "places")
    places_field.send_keys("3")
    form = driver.find_element(By.TAG_NAME, "form")
    form.submit()


def logout():
    logout_link = driver.find_element(By.LINK_TEXT, "Logout")
    logout_link.click()


def test_run_functional():
    inject_test_data()
    visit_homepage()
    navigate_to_club_board()
    login("test@example.com")
    navigate_to_club_board()
    book_places_for_competition()
    logout()
