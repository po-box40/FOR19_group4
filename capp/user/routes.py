from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user
from capp import db, bcrypt
from capp.models import User
from capp.user.forms import RegistrationForm, LoginForm


app = Flask(__name__)


@app.route("/register", methods=["GET", "POST"])
def register():
    # check if the user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":
        form = RegistrationForm()
        # enctrypt the password
        hashed_password = bcrypt.generate_password_hash(
            request.form["password"]
        ).decode("utf-8")
        # Extract form data using request.form
        if form.validate_on_submit():
            user = User(
                username=request.form["username"],
                email=request.form["email"],
                password=hashed_password,
            )
            db.session.add(user)
            db.session.commit()
            flash(
                "Your account has been created! You are now able to log in", "success"
            )

        # Perform registration logic
        return redirect(url_for("login"))
    else:
        # Render registration form
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # check if the user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for("home.home_home"))

    if request.method == "POST":
        # Handle login form submission
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=request.form["email"]).first()
            if user and bcrypt.check_password_hash(
                user.password, request.form["password"]
            ):
                login_user(user)
                # add next page functionality
                next_page = request.args.get("next")
                # flash login message to user
                flash("Login Successful", "success")

                if next_page:
                    return redirect(next_page)

                else:
                    return redirect(url_for("home.home_home"))

            else:
                flash("Login Unsuccessful. Please check email and password", "danger")
        # Extract form data using request.form
        # Perform login logic
        return redirect(url_for("dashboard"))
    else:
        # Render login form
        return render_template("login.html")


@app.route("/logout")
def logout():
    # Perform logout logic
    logout_user()
    return redirect(url_for("home.home_home"))


if __name__ == "__main__":
    app.run()
