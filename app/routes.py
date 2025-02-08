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
        flash("Email is required")
        return redirect(request.referrer)

    clubs = current_app.clubs
    competitions = current_app.competitions

    club = next((club for club in clubs if club["email"] == email), None)
    if club is None:
        flash("Email not found")
        return redirect(request.referrer)

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


# @main.route("/purchasePlaces", methods=["POST"])
# def purchasePlaces():
#     competition = [c for c in competitions if c["name"] == request.form["competition"]][
#         0
#     ]
#     club = [c for c in clubs if c["name"] == request.form["club"]][0]
#     placesRequired = int(request.form["places"])
#     competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - placesRequired
#     flash("Great-booking complete!")
#     return render_template("welcome.html", club=club, competitions=competitions)


# TODO: Add route for points display


@main.route("/logout")
def logout():
    return redirect(url_for("main.index"))
