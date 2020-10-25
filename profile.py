from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app, send_from_directory
    )
from werkzeug.exceptions import abort
import os
from werkzeug.utils import secure_filename

from flaskr.auth import login_required
from flaskr.db import get_db

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', "png"}

bp = Blueprint("profile", __name__,url_prefix="/profile")

@bp.route("/<int:userid>", methods=("GET","POST"))
@login_required
def profile(userid):
    
    user = get_user(userid)
    posts = get_user_posts(userid)
    print(user["joindate"])

    db = get_db()
    avatar_id = db.execute(" SELECT avatar_id FROM user where id = ?", (userid,)).fetchone()
    print(avatar_id)
    print(avatar_id[0])

    if avatar_id[0] == 0:
        return render_template("profile/main.html", user=user, posts=posts, filename="default.jpg")
    
    filename = get_user_avatar(userid)
    print(send_from_directory(current_app.config['UPLOAD_PATH'], filename))

    return render_template("profile/main.html", user=user, posts=posts, filename=filename)


@bp.route("/<int:userid>/bio/update", methods=("GET","POST"))
@login_required
def edit_bio(userid):
    
    bio = get_bio(userid)
    user = get_user(userid)
    

    
    if request.method == "POST":
        body = request.form["bio"]
        error = None
        db = get_db()
        db.execute("UPDATE user SET bio = ? WHERE id = ?", (body, userid))
        db.commit()
        return redirect(url_for("profile.profile", userid = userid))

    return render_template("profile/edit_bio.html", user=user)


def get_bio(userid, check_user=True):
    bio = get_db().execute(
        " SELECT bio from USER where id=?", (userid,)
    ).fetchone()

    if check_user and userid != g.user["id"]:
        abort(403)

    return bio

def get_user(userid):
    user = get_db().execute(
        " SELECT * from USER where id=?", (userid,)
    ).fetchone()
    return user

def get_user_posts(userid):
    posts = get_db().execute(
        "SELECT * from post WHERE author_id=?", (userid,)
        ).fetchall()
    return posts

def get_user_avatar(userid):
    db = get_db()
    avatar_id = db.execute("SELECT avatar_id FROM user where id = ?", (userid,)).fetchone()[0]
    filename = db.execute("SELECT picture_path FROM pictures where picture_id = ? ", (avatar_id,)).fetchone()[0]
    return filename


def set_user_avatar(filename, userid):
    db = get_db()
    avatar_id = db.execute("SELECT picture_id FROM pictures where picture_path = (?)", (filename,)).fetchone()
    avatar_id = avatar_id[0]
    db.execute("UPDATE User SET avatar_id = ? WHERE id = ?", (avatar_id, userid,))
    db.commit()

@bp.route("/<int:userid>/avatar/update", methods=["GET","POST"])
@login_required
def change_avatar(userid):
    
    db = get_db()
    user = get_user(userid)
    allowed_file("hi")

    if request.method == "POST":
        print(request.files.get("file"))

        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        
        file = request.files["file"]
        if file.filename == "":
            flash("No selected file")

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            picture_path = "http://127.0.0.1:5000/uploads/" + filename
            file.save(os.path.join(current_app.config['UPLOAD_PATH'], filename))
            db.execute("INSERT INTO pictures (picture_path) VALUES (?);", (filename,))
            set_user_avatar(filename, userid)
            db.commit()
            return redirect(url_for("profile.profile", userid=userid, filename=filename))

    return render_template("profile/change_avatar.html", user=user)

def allowed_file(filename):
    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/uploads/<filename>')
def send_file(filename):
    print("file: ", send_from_directory(current_app.config['UPLOAD_PATH'], filename))
    return send_from_directory(current_app.config['UPLOAD_PATH'], filename)