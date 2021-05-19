from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import Test

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/test')
def test():
    return render_template('test.html')

@main.route('/test', methods=['POST'])
def signup_post():
    something = request.form.get('something')
    flash('Here is what you write: ',something)
    
    new_content = Test(content=something)

    db.session.add(new_content)
    db.session.commit()

    
#    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

#    if user: # if a user is found, we want to redirect back to signup page so user can try again
#        flash('Email address already exists')
#        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
#    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
#    db.session.add(new_user)
#    db.session.commit()

    return redirect(url_for('main.test'))
    
