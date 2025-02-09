import json
from flask import (
    Blueprint,
    current_app,
    render_template,
    request,
    redirect,
    flash,
    url_for,
    session,
)


main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/login", methods=["POST"])
def login():
    email = request.form["email"]

    if not email:
        flash("Email is required.")
        return render_template("index.html")

    clubs = current_app.clubs
    club = next((club for club in clubs if club["email"] == email), None)

    if club is None:
        flash("Email not found.")
        return render_template("index.html")

    session["club_name"] = club["name"]
    return redirect(url_for("main.home"))


@main.route("/home", methods=["GET"])
def home():
    club_name = session.get("club_name")
    clubs = current_app.clubs
    competitions = current_app.competitions

    club = next((club for club in clubs if club["name"] == club_name))

    return render_template("welcome.html", club=club, competitions=competitions)


@main.route("/book/<competition>/<club>")
def book(competition, club):
    clubs = current_app.clubs
    competitions = current_app.competitions
    found_club = [c for c in clubs if c["name"] == club][0]
    found_competition = [c for c in competitions if c["name"] == competition][0]
    if found_club and found_competition:
        return render_template(
            "booking.html", club=found_club, competition=found_competition
        )
    else:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions)


@main.route("/purchasePlaces", methods=["POST"])
def purchase_places():
    # Retrieve the list of clubs and competitions
    clubs = current_app.clubs
    competitions = current_app.competitions

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

    if places_required <= 0:
        flash("Please enter a number greater than zero")
        return render_template("booking.html", club=club, competition=competition)

    elif (places_already_booked + places_required) > 12:
        flash(
            f"You cannot book more than 12 places for '{competition['name']}' competition"
        )
        return render_template("booking.html", club=club, competition=competition)

    elif places_required > club_points:
        point_label = "point" if club_points == 1 else "points"
        flash(f"Sorry, your club has {club_points} {point_label} left")
        return render_template("booking.html", club=club, competition=competition)

    elif places_required > places_available:
        places_label = "place" if places_available == 1 else "places"
        flash(f"Sorry, the competition has {places_available} {places_label} left")
        return render_template("booking.html", club=club, competition=competition)

    club["points"] = str(club_points - places_required)
    competition["numberOfPlaces"] = str(places_available - places_required)

    if "places_already_booked" not in club:
        club["places_already_booked"] = {}

    club["places_already_booked"][competition["name"]] = (
        club["places_already_booked"].get(competition["name"], 0) + places_required
    )

    # Update club points
    with open("data/clubs.json", "w") as file:
        json.dump({"clubs": clubs}, file)

    # Update competition places
    with open("data/competitions.json", "w") as file:
        json.dump({"competitions": competitions}, file)

    flash("Great - booking complete!")
    return render_template("welcome.html", club=club, competitions=competitions)


@main.route("/logout")
def logout():
    return redirect(url_for("main.index"))
