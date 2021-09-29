from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, current_app
from flask_login import login_required, current_user

from . import db
from .models import Test, Point #, PointSchema

from .db_conn import saveMyData, getMyPoints

import json

import os.path
import sqlite3

from werkzeug.utils import secure_filename

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


############################ db ############################################
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


################################### test #######################################

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

########################### upload #############################################
UPLOAD_FOLDER = 'project/static/data/'
ALLOWED_EXTENSIONS = {'gpx', 'txt'}

#current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/upload', methods=['GET', 'POST'])
def upload_file():
    current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    if request.method == 'POST':
        # check if the post request has the file part
        print (request.files)
        if 'file' not in request.files:
            flash('No file part')
            print('Nothing inside')
            print(request.url)
            #return redirect(request.url)
        file = request.files['file']
        print (file)
        print ("Filename:", file.filename)
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            print('No selected file')
            return redirect(request.url)
        print (allowed_file(file.filename))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'],filename))
            print('saved file somewhere')
            #return redirect(url_for('download_file', name=filename))
    return render_template('upload.html', name=current_user.name)
    

################################################################################


    
#if __name__ == '__main__':
    
#app.run
#(host='0.0.0.0') 
##Stevie says:* Running on 
#http://0.0.0.0:5000/
 