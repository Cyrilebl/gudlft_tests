import os
import json
import secrets
from datetime import datetime
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    url_for,
    session,
    jsonify,
)

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)


def load_json(file_name):
    file_path = os.path.join("data", file_name)
    with open(file_path) as file:
        return json.load(file)


def load_clubs():
    return load_json("clubs.json")["clubs"]


def load_competitions():
    return load_json("competitions.json")["competitions"]


# Load data
clubs = load_clubs()
competitions = load_competitions()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/club-board")
def club_board():
    return render_template("club-board.html", clubs=clubs)


@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    try:
        club = [c for c in clubs if c["email"] == email][0]
        session["club"] = club["name"]
        return redirect(url_for("home"))

    except IndexError:
        if request.form["email"] == "":
            flash("Email is required")
        else:
            flash("Email not found")
        return render_template("index.html")


@app.route("/home")
def home():
    club_name = session.get("club")
    club = next((c for c in clubs if c["name"] == club_name), None)
    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/book/<club>/<competition>")
def book(competition, club):
    found_club = next((c for c in clubs if c["name"] == club), None)
    found_competition = next(
        (c for c in competitions if c["name"] == competition), None
    )
    if found_club and found_competition:
        return render_template(
            "booking.html", club=found_club, competition=found_competition
        )
    else:
        flash("Something went wrong - Please try again")
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/purchase-places", methods=["POST"])
def purchase_places():
    # Find the selected club and competition based on the submitted form data
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    competition = [c for c in competitions if c["name"] == request.form["competition"]][
        0
    ]

    # Get the number of places requested
    places_required = request.form["places"]
    if not places_required:
        flash("Please enter a number")
        return render_template("booking.html", club=club, competition=competition)

    places_required = int(places_required)
    club_points = int(club["points"])
    places_available = int(competition["numberOfPlaces"])

    places_already_booked = int(
        club.get("places_already_booked", {}).get(competition["name"], 0)
    )

    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    competition_date = competition["date"]
    competition_date_object = datetime.strptime(competition_date, "%Y-%m-%d %H:%M:%S")
    formatted_date = competition_date_object.strftime("%B %d, %Y, at %H:%M %p")

    error_message = None

    if places_required <= 0:
        error_message = "Please enter a number greater than zero"

    elif current_date > competition_date:
        error_message = f"This competition already took place on {formatted_date}"

    elif (places_already_booked + places_required) > 12:
        error_message = f"You cannot book more than 12 places for '{competition['name']}' competition"

    elif places_required > club_points:
        point_label = "point" if club_points == 1 else "points"
        error_message = f"Sorry, your club has {club_points} {point_label} left"

    elif places_required > places_available:
        places_label = "place" if places_available == 1 else "places"
        error_message = (
            f"Sorry, the competition has {places_available} {places_label} left"
        )

    if error_message:
        flash(error_message)
        return render_template("booking.html", club=club, competition=competition)

    club["points"] = str(club_points - places_required)
    competition["numberOfPlaces"] = str(places_available - places_required)

    if "places_already_booked" not in club:
        club["places_already_booked"] = {}

    club["places_already_booked"][competition["name"]] = (
        club["places_already_booked"].get(competition["name"], 0) + places_required
    )

    if not app.config["TESTING"]:
        # Update club points
        with open("data/clubs.json", "w") as file:
            json.dump({"clubs": clubs}, file)

        # Update competition places
        with open("data/competitions.json", "w") as file:
            json.dump({"competitions": competitions}, file)

    flash("Great - booking complete!")
    return redirect(url_for("home"))


@app.route("/logout")
def logout():
    return redirect(url_for("index"))


@app.route("/set-test-data", methods=["POST"])
def set_test_data():
    app.config["TESTING"] = request.json.get("testing", False)
    global clubs, competitions
    clubs = request.json.get("clubs", [])
    competitions = request.json.get("competitions", [])
    return jsonify({"message": "Test data successfully set"})


if __name__ == "__main__":
    app.run(debug=True)
