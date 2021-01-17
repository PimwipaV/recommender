FROM python:latest

LABEL maintainer="pimpwhippa<utrechtmay@gmail.com>"

WORKDIR /box
COPY . /box
COPY templates templates
RUN pip install -r requirements.txt
#RUN /usr/bin/sqlite3 /box/test.db
CMD ["python","app.py"]
#ถ้าไ่ม่ใส่อะไรเลยก็ docker exec -it เข้าได้ปกติ ibobox bash
#CMD ["flask", "run", "--host", "0.0.0.0"]