FROM ubuntu:latest
# Maintainer: Sebastian
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update

RUN apt-get update
RUN apt-get -y install curl gnupg
RUN curl -sL https://deb.nodesource.com/setup_14.x  | bash -
RUN apt-get -y install nodejs
RUN apt -y install git
RUN npm install -g npm
RUN apt -y install python3-pip python3-dev build-essential
RUN apt update && apt upgrade -y

RUN pip3 install --upgrade pip
RUN pip3 install flask numpy requests pandas psycopg2-binary mysql-connector-python pymysql
RUN pip3 install flask_login flask_sqlalchemy marshmallow-sqlalchemy flask-marshmallow

RUN git clone https://github.com/mightyMarabu/flask_auth_app.git

RUN cd flask_auth_app/project/

WORKDIR /flask_auth_app/project

RUN npm install 
RUN npm run build
#RUN npm install --save-dev webpack
#RUN npm install ol --save

EXPOSE 80 5000

ENV NAME world
#CMD [ "npm", "run", "watch" ]
#RUN npm run build
#RUN cd ..
#CMD ["sh", "flask_auth_app/start.sh"]
#RUN export FLASK_APP=project 
#RUN flask run
#ENTRYPOINT [ "flask" ]
CMD ["flask","run", "--host=0.0.0.0", "--port=5000"]
