import os
import json
import random
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
from flask import Flask, render_template, request, redirect, Response, flash, Blueprint
from spotify import get_artist_info
from genius import get_lyrics
from flask_login import (
    LoginManager,
    login_required,
    current_user,
    login_user,
    logout_user,
    UserMixin,
)
from flask_sqlalchemy import SQLAlchemy

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


class Person(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    artists = db.relationship("Artist", backref="person", lazy=True)

    def __repr__(self):
        return "<Username: {}>".format(self.username)

    def get_id(self):
        return self.id


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.String(22))
    person_id = db.Column(db.Integer, db.ForeignKey("person.id"))

    def __repr__(self):
        return "<Artist Id: {}>".format(self.artist_id)


bp = Blueprint("bp", __name__, template_folder="./build")


@bp.route("/index")
@login_required
def index():
    # TODO: insert the data fetched by your app main page here as a JSON
    DATA = {"your": "data here"}
    data = json.dumps(DATA)
    return render_template(
        "index.html",
        data=data,
    )


app.register_blueprint(bp)

login = LoginManager()
login.init_app(app)
login.login_view = "login"


@login.user_loader
def load_user(id):
    return Person.query.get(id)


@app.errorhandler(401)
def page_not_found(e):
    return Response("<p>Login failed</p>")


@app.before_first_request
def create_table():
    db.create_all()


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        username = request.form["username"]
        user = Person.query.filter_by(username=username).first()
        if user is not None:
            login_user(user)
            return redirect("/")
        if user is None:
            flash("Invalid username!")
    return render_template("login.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect("/")

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


@app.route("/", methods=["POST", "GET"])
@login_required
def index():
    currentUser = Person.query.filter_by(username=current_user.username).first()
    if request.method == "POST":
        artistID = request.form.get("artistId")
        try:
            get_artist_info(artistID)
        except:
            flash("Invalid Spotify Artist ID!")
            return redirect("/")

        artist = Artist(artist_id=artistID, person=currentUser)

        db.session.add(artist)
        db.session.commit()

        flash("Artist added!")

    user_artists = currentUser.artists
    user_artist_ids = []
    for artists in user_artists:
        if artists.artist_id not in user_artist_ids:
            user_artist_ids.append(artists.artist_id)

    try:
        ARTIST_IDS = user_artist_ids
        artist_len = len(ARTIST_IDS)
        random_artist = random.randint(0, artist_len - 1)

    except:
        ARTIST_IDS = ["5cj0lLjcoR7YOSnhnX0Po5"]  # doja cat
        artist_len = 0
        random_artist = 0

    artist = ARTIST_IDS[random_artist]
    (name, img, track, topTracks) = get_artist_info(artist)
    (trackName, trackAudio, trackImg) = track
    lyricLink = get_lyrics(name, trackName)

    return render_template(
        "music.html",
        artist_len=artist_len,
        name=name,
        img=img,
        len=len(topTracks),
        topTracks=topTracks,
        track=track,
        trackName=trackName,
        trackImg=trackImg,
        trackAudio=trackAudio,
        lyricLink=lyricLink,
    )


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


app.run(
    host=os.getenv("0.0.0.0"),
    port=int(os.getenv("PORT", 8081)),
)
