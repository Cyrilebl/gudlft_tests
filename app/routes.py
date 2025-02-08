import json
from flask import (
    Blueprint,
    current_app,
    render_template,
    request,
    redirect,
    flash,
    url_for,
)


main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/home", methods=["POST"])
def home():
    email = request.form["email"]

    if not email:
        flash("Email is required.")
        return redirect(url_for("main.index"))

    clubs = current_app.clubs
    competitions = current_app.competitions

    club = next((club for club in clubs if club["email"] == email), None)
    if club is None:
        flash("Email not found.")
        return redirect(url_for("main.index"))

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
def purchasePlaces():
    clubs = current_app.clubs
    competitions = current_app.competitions

    competition = [c for c in competitions if c["name"] == request.form["competition"]][
        0
    ]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]

    places_required = request.form["places"]
    if not places_required:
        flash("Please enter a number")
        return redirect(request.referrer)

    places_required = int(places_required)
    club_points = int(club["points"])
    places_available = int(competition["numberOfPlaces"])

    if places_required <= 0:
        flash("Please enter a number greater than zero")
        return redirect(request.referrer)

    elif places_required > club_points:
        point_label = "point" if club_points == 1 else "points"
        flash(f"Sorry, your club has {club_points} {point_label} left")
        return redirect(request.referrer)

    elif places_required > places_available:
        places_label = "place" if club_points == 1 else "places"
        flash(f"Sorry, only {places_available} {places_label} left")
        return redirect(request.referrer)

    club["points"] = str(club_points - places_required)
    competition["numberOfPlaces"] = str(places_available - places_required)

    # Update club points
    with open("data/clubs.json", "w") as file:
        json.dump({"clubs": clubs}, file)

    # Update competition places
    with open("data/competitions.json", "w") as file:
        json.dump({"competitions": competitions}, file)

    flash("Great - booking complete!")
    return render_template("welcome.html", club=club, competitions=competitions)


# TODO: Add route for points display


@main.route("/logout")
def logout():
    return redirect(url_for("main.index"))
