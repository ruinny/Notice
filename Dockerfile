FROM python:3.6
RUN mkdir -p /usr/src/notice_env
#COPY pip.conf /root/.pip/pip.conf
COPY requirements.txt /usr/src/notice_env
RUN pip install -r /usr/src/notice_env/requirements.txt
RUN mkdir -p /usr/src/notice
WORKDIR /usr/src/notice
CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8080"]