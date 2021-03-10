FROM tensorflow/tensorflow:latest

LABEL maintainer="pimpwhippa<utrechtmay@gmail.com>"

WORKDIR /box
COPY . /box
COPY templates templates
RUN pip install -r requirements.txt
#RUN /usr/bin/sqlite3 /box/test.db
RUN useradd -ms /bin/bash 1000
USER 1000
#WORKDIR /home/1000
CMD ["python","app.py"]

#export FLASK_APP=app.py
#ENV FLASK_ENV="docker"
#CMD ["flask", "run", "--host", "0.0.0.0"]
