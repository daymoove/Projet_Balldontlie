from flask import Blueprint, render_template, request, session, redirect, url_for
from flask_login import login_required, current_user
import requests
import json

teams = Blueprint('teams', __name__)

@teams.route('/teams',methods=['GET','POST'])
@login_required
def Teams():
    return render_template("teams.html", user=current_user)