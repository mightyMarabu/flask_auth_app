#!/bin/bash
cd flask_auth_app/project
npm run build
cd ..

export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export FLASK_APP=project
export FLASK_DEBUG=1
flask run
