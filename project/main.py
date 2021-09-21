from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user

from . import db
from .models import Test, Point #, PointSchema

from .db_conn import saveMyData, getMyPoints

import json

import os.path
import sqlite3

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/contact')
@login_required
def contact():
    return render_template('contact.html', name=current_user.name)

@main.route('/test')
def test():
    return render_template('test.html')

@main.route('/test', methods=['POST'])
def form_post():
    something = request.form.get('something')
    #flash('Here is what you write: ',something)
    new_content = Test(content=something)
    db.session.add(new_content)
    db.session.commit()
    return jsonify("Data saved to sqlite-DB!")


########################################################################
@main.route('/savePoint/<x>/<y>/<pointName>/', methods=['POST','GET'])
def saveMyPoint(x,y,pointName):
    #something = request.form.get('something')
    #flash('Here is what you write: ',something)
    new_point = Point(lng=x, lat=y, name=pointName)
    db.session.add(new_point)
    db.session.commit()
    return jsonify("Point saved!")

@main.route('/getPoints', methods=['POST','GET'])
def getPoints():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "db.sqlite")
    with sqlite3.connect(db_path) as db:
        #connection = sqlite3.connect("db.sqlite") 
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Point;") 
        result = cursor.fetchall() 
        print (result)
        points = []
        for r in result:
            print (r)
            point = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [r[1], r[2]]
                        },
                    "properties": {
                        "name": r[3],
                        "description" : r[4]
                        }
                    }
            #print (point)
            points.append(point)           
        #print (points)
        geojson = {"type": "FeatureCollection",
                   "crs": {"type": "name",
                            "properties": {
                            "name": "EPSG:4326",
                            }
                        },
                    "features": points
        }
        print (geojson)
        return geojson, {'ContentType':'application/json'}


##########################################################################

@main.route('/test1', methods=['POST'])
def json_post():
    someJson = request.form
    #flash('Here is what you write: ',someJson)
    print (someJson)
    return jsonify(someJson, "this was saved...")

@main.route('/test2', methods=['POST'])
def db_post():
    someJson = request.form
    #flash('Here is what you write: ',someJson)
    print (someJson)
    someJson = json.dumps(someJson)
    saveMyData(someJson)
    return jsonify("Data saved!")

@main.route('/test3', methods=['POST'])
def saveMyJsonToPostgres():
    myJson = request.get_json()
    print(myJson)
    myJson = json.dumps(myJson)
    saveMyData(myJson)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    #return jsonify("data saved!")

  


    
#if __name__ == '__main__':
    
#app.run
#(host='0.0.0.0') 
##Stevie says:* Running on 
#http://0.0.0.0:5000/
 