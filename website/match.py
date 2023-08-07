from flask import Blueprint, render_template, request, session, redirect, url_for
from flask_login import login_required, current_user
import requests
import json

match = Blueprint('match', __name__)

@match.route('/matchs',methods=['GET','POST'])
@login_required
def Matchs():
    return render_template("Matchs.html", user=current_user)