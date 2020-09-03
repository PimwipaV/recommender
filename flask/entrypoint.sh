#!/bin/sh
FROM ubuntu
MAINTAINER pimpwhippa
RUN apt-get update
ENTRYPOINT [“echo”, “Hello World”]