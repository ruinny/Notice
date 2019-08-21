FROM python:3.6
RUN mkdir -p /usr/src/notice/docker
RUN mkdir -p /usr/src/notice/app
#COPY pip.conf /root/.pip/pip.conf
COPY requirements.txt /usr/src/notice/docker
RUN pip install -r /usr/src/notice/docker/requirements.txt
WORKDIR /usr/src/notice/app
CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8080"]