from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    from .models import User
    from . import db  
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('logged in succesfully.', category='succes')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else :
                flash('incorect try again.',category= 'error')
        else:
            flash('Email does not exist.',category= 'error')
            
                      
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    from .models import User
    from . import db  
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user: 
            flash('Email already exist', category='error')
        elif password1 != password2 :
            flash('password does not match.', category='error')
        elif email == "" or first_name == "" or password1 == "" or password2 == "":
            flash('One or more information are missing.', category='error')
        else:

            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Account created.', category='succes')
            return redirect(url_for('views.home'))

    return render_template("signIn.html", user=current_user)

