FROM mysql/mysql-server:latest

LABEL maintainer="pimpwhippa<utrechtmay@gmail.com>"

WORKDIR /recommender
ADD . /recommender
RUN ["apt-get", "update"]
RUN ["apt-get", "install", "-y", "nano"]
ENV TERM xterm