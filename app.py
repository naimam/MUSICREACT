# pylint: disable=E1101, C0413, W1508, W0703, R0903, R0914, W0603, W0632
"""
    This is the main file for the application.
    It contains the db models and the routes for the application.
"""
import os
import json
import random
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    Blueprint,
    url_for,
    json,
    jsonify,
)
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    login_required,
    current_user,
    login_user,
    logout_user,
    UserMixin,
)
from spotify import get_artist_info
from genius import get_lyrics

app = Flask(__name__, static_folder="./build/static")

load_dotenv(find_dotenv())
url = os.getenv("DATABASE_URL")
if url and url.startswith("postgres://"):
    url = url.replace("postgres://", "postgresql://", 1)

SECRET_KEY = os.getenv("SECRET_KEY")

app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["SQLALCHEMY_DATABASE_URI"] = url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = SECRET_KEY

db = SQLAlchemy()
db.init_app(app)

# db model
class Person(db.Model, UserMixin):
    """Person model"""

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    artists = db.relationship("Artist", backref="person", lazy=True)

    def __repr__(self):
        return "<Username: {}>".format(self.username)

    def get_id(self):
        return self.user_id


class Artist(db.Model):
    """Artist model"""

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.String(22))
    person_id = db.Column(db.Integer, db.ForeignKey("person.user_id"))

    def __repr__(self):
        return "<Artist Id: {}>".format(self.artist_id)


# routes
bp = Blueprint("bp", __name__, template_folder="./build")


@bp.route("/index", methods=["POST", "GET"])
@login_required
def index():
    """index route: main page of app"""
    user = Person.query.filter_by(username=current_user.username).first()
    current_username = current_user.username
    user_artists = user.artists
    user_artist_ids = []
    for artists in user_artists:
        user_artist_ids.append(artists.artist_id)

    has_artists_saved = len(user_artist_ids) > 0
    if has_artists_saved:
        artist_len = len(user_artist_ids)
        random_artist = random.randint(0, artist_len - 1)
        artist = user_artist_ids[random_artist]
        (artist_name, artist_img, track) = get_artist_info(artist)
        (track_name, track_audio, track_img) = track
        lyric_link = get_lyrics(track_name)

    else:
        (
            artist_name,
            artist_img,
            track,
            track_name,
            track_img,
            track_audio,
            lyric_link,
        ) = (
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        )
    user_data = {
        "current_username": current_username,
        "has_artists_saved": has_artists_saved,
        "user_artist_ids": user_artist_ids,
        "artist_name": artist_name,
        "artist_img": artist_img,
        "track": track,
        "track_name": track_name,
        "track_img": track_img,
        "track_audio": track_audio,
        "lyric_link": lyric_link,
    }
    data = json.dumps(user_data)
    return render_template(
        "index.html",
        data=data,
    )


app.register_blueprint(bp)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    """user loader"""
    return Person.query.get(user_id)


@app.before_first_request
def create_table():
    """create table"""
    db.create_all()


@app.route("/login", methods=["POST", "GET"])
def login():
    """login route: login page of app"""
    if current_user.is_authenticated:
        return redirect(url_for("bp.index"))

    if request.method == "POST":
        username = request.form["username"]
        user = Person.query.filter_by(username=username).first()
        if user is not None:
            login_user(user)
            return redirect(url_for("bp.index"))
        if user is None:
            flash("Invalid username!")
    return render_template("login.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    """register route: register page of app"""
    if current_user.is_authenticated:
        return redirect(url_for("bp.index"))

    if request.method == "POST":
        username = request.form["username"]

        if Person.query.filter_by(username=username).first():
            flash("Username is taken!")
            return redirect("/register")

        user = Person(username=username)
        db.session.add(user)
        db.session.commit()
        flash("Account creation successful!")
        return redirect("/login")
    return render_template("register.html")


@app.route("/")
def main():
    """main route: redirects to index page"""
    if current_user.is_authenticated:
        return redirect(url_for("bp.index"))
    return redirect("/login")


@app.route("/logout")
def logout():
    """logout route: logouts user"""
    logout_user()
    return redirect(url_for("bp.index"))


@app.route("/save", methods=["POST", "GET"])
def save():
    """save route: updates users artists in db"""
    user = Person.query.filter_by(username=current_user.username).first()
    artists_to_add = []
    add_artists = request.json.get("add")
    artists_to_remove = request.json.get("delete")
    success_message = []
    failure_message = ""
    if add_artists:
        for artist in add_artists:
            if artist not in user.artists:
                try:
                    get_artist_info(artist)
                except Exception:
                    failure_message = "Invalid artist id(s)!"
                    continue
                artists_to_add.append(artist)

    if artists_to_add:
        for artist in artists_to_add:
            new_artist = Artist(artist_id=artist, person_id=user.user_id)
            db.session.add(new_artist)
            db.session.commit()
        success_message.append("Artist(s) added!")

    if artists_to_remove:
        for artist in artists_to_remove:
            delete_artist = Artist.query.filter_by(artist_id=artist).first()
            if delete_artist is not None:
                db.session.delete(delete_artist)

        db.session.commit()
        success_message.append("Artist(s) removed!")

    current_user_artists = user.artists
    current_user_artist_ids = []
    for artists in current_user_artists:
        current_user_artist_ids.append(artists.artist_id)

    print("failure msg:", failure_message)
    print("success msg:", success_message)
    return jsonify(
        {
            "user_artists_server": current_user_artist_ids,
            "failure_message": failure_message,
            "success_message": success_message,
        }
    )


app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
