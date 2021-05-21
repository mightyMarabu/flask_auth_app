from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from . import db
from .models import Test

from .db_conn import saveMyData

import json

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
def form_post():
    something = request.form.get('something')
    flash('Here is what you write: ',something)
    
    new_content = Test(content=something)

    db.session.add(new_content)
    db.session.commit()

@main.route('/test1', methods=['POST'])
def json_post():
    someJson = request.form
    #flash('Here is what you write: ',someJson)
    print (someJson)
    return jsonify(someJson)

@main.route('/test2', methods=['POST'])
def db_post():
    someJson = request.form
    #flash('Here is what you write: ',someJson)
    print (someJson)
    someJson = json.dumps(someJson)
    saveMyData(someJson)
    return jsonify("Data saved!")
  
  

 #   return redirect(url_for('main.test'))
    
