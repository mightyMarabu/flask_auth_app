FROM ubuntu:latest
# Maintainer: Sebastian
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update
RUN apt -y install git npm
RUN apt -y install python3-pip python3-dev build-essential

WORKDIR /

RUN pip3 install --upgrade pip
RUN pip3 install flask numpy requests pandas psycopg2-binary mysql-connector-python pymysql
RUN pip3 install flask_login

RUN git clone https://github.com/mightyMarabu/flask_auth_app.git

RUN cd flask_auth_app/project/ && npm install --save-dev webpack && npm install ol --save

#RUN npm install --save-dev webpack
#RUN npm install ol --save

EXPOSE 80

ENV NAME world
CMD [ "npm", "run", "watch" ]
#RUN npm run watch
RUN cd ..
CMD ["python3","flask_auth_app/project/main.py"]
#RUN export FLASK_APP=project
#RUN flask run