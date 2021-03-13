from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from flask_login import login_user, login_required, logout_user, current_user

from app.extensions import login_manager
from app.models import User, db, Store
from app.forms import SignupForm, LoginForm

user_bp = Blueprint('user', __name__)


@user_bp.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("You are already logged in", 'warning')
        return redirect(url_for("products.index"))

    form = SignupForm()
    if form.validate_on_submit():
        user = User.create(form.email.data, form.password.data)
        db.session.add(user)
        store = Store(name=form.store_name.data, user=user)
        db.session.add(store)
        db.session.commit()

        login_user(user)
        flash("Registered succesfully.", "success")

        return redirect(session.get('after_login') or url_for("products.index"))
    return render_template("users/register.html", form=form)


@user_bp.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in", 'warning')
        return redirect(url_for("products.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user)
        flash("Logged in successfully.", "success")
        return redirect(url_for("products.index"))

    return render_template("users/login.html", form=form)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    session['after_login'] = request.url
    return redirect(url_for('user.login'))


@user_bp.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('products.index'))

