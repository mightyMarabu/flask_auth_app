#!/bin/bash
cd flask_auth_app/project
#cd project
npm run build
cd ..

export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export FLASK_APP=project
export FLASK_DEBUG=0
export host=0.0.0.0
flask run
