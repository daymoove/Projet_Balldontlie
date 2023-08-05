from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("home.html", user=current_user)

@views.route('/player')
@login_required
def player():
    return render_template("Player.html", user=current_user)

@views.route('/teams')
@login_required
def teams():
    return render_template("Teams.html", user=current_user)

@views.route('/Matchs')
@login_required
def Matchs():
    return render_template("Matchs.html", user=current_user)