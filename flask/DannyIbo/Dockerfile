FROM python:latest

LABEL maintainer="pimpwhippa<utrechtmay@gmail.com>"

WORKDIR /box
COPY . /box
RUN pip install -r requirements.txt
CMD ["python","app.py"]
#พอใส่ CMD ไปบรรทัดนึง แม่งไม่รันเลย รันไม่ขึ้น
#ถ้าไ่ม่ใส่อะไรเลยก็ docker exec -it เข้าได้ปกติ ibobox bash
#CMD ["bash"]