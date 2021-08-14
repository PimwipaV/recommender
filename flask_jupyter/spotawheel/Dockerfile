FROM jupyter/tensorflow-notebook:latest
LABEL maintainer="pimpwhippa<utrechtmay@gmail.com>"
WORKDIR /jupyter
ADD . /jupyter
RUN pip install -r requirements.txt
#RUN ["apt-get", "update"]
#RUN ["apt-get", "install", "-y", "nano"]
ENV TERM xterm
