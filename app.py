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
    Response,
    flash,
    Blueprint,
    url_for,
    json,
    jsonify,
)
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

# db model
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


# routes
bp = Blueprint("bp", __name__, template_folder="./build")


@bp.route("/index", methods=["POST", "GET"])
@login_required
def index():
    currentUser = Person.query.filter_by(username=current_user.username).first()
    current_username = current_user.username
    user_artists = currentUser.artists
    user_artist_ids = []
    for artists in user_artists:
        user_artist_ids.append(artists.artist_id)

    has_artists_saved = len(user_artist_ids) > 0
    if has_artists_saved:
        artist_len = len(user_artist_ids)
        random_artist = random.randint(0, artist_len - 1)
        artist = user_artist_ids[random_artist]
        (name, img, track) = get_artist_info(artist)
        (trackName, trackAudio, trackImg) = track
        lyricLink = get_lyrics(trackName)

    else:
        (artist_len, name, img, track, trackName, trackImg, trackAudio, lyricLink) = (
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        )
    DATA = {
        "current_username": current_username,
        "has_artists_saved": has_artists_saved,
        "user_artist_ids": user_artist_ids,
        "name": name,
        "img": img,
        "track": track,
        "trackName": trackName,
        "trackImg": trackImg,
        "trackAudio": trackAudio,
        "lyricLink": lyricLink,
    }
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


@app.before_first_request
def create_table():
    db.create_all()


@app.route("/login", methods=["POST", "GET"])
def login():
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
    if current_user.is_authenticated:
        return redirect(url_for("bp.index"))
    return redirect("/login")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("bp.index"))


@app.route("/save", methods=["POST", "GET"])
def save():
    currentUser = Person.query.filter_by(username=current_user.username).first()
    artists_to_add = []
    add_artists = request.json.get("add")
    artists_to_remove = request.json.get("delete")
    print("og artists:", currentUser.artists)
    print("add:", add_artists)
    if add_artists:
        for artist in add_artists:
            if artist not in currentUser.artists:
                try:
                    get_artist_info(artist)
                except:
                    continue
                artists_to_add.append(artist)
    print("artists to add:", artists_to_add)
    if artists_to_add:
        for artist in artists_to_add:
            new_artist = Artist(artist_id=artist, person_id=currentUser.id)
            db.session.add(new_artist)
            db.session.commit()
            jsonify({"status": "Artist(s) added!"})

    if artists_to_remove:
        for artist in artists_to_remove:
            delete_artist = Artist.query.filter_by(artist_id=artist).first()
            if delete_artist is not None:
                db.session.delete(delete_artist)

        print("artists to remove:", artists_to_remove)
        db.session.commit()
        jsonify({"status": "Artist(s) removed!"})

    current_user_artists = currentUser.artists
    current_user_artist_ids = []
    for artists in current_user_artists:
        current_user_artist_ids.append(artists.artist_id)

    print("updated artists:", current_user_artist_ids)
    return jsonify({"user_artists_server": current_user_artist_ids})


app.run(
    host=os.getenv("0.0.0.0"),
    port=int(os.getenv("PORT", 8081)),
)
