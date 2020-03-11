FROM python:3.6-buster 
RUN pip3 install Flask
RUN pip3 install flask-mysqldb
RUN pip3 install requests
RUN pip3 install redis
RUN mkdir templates
COPY templates/input.html templates/
COPY CodFuente.py /

ENV FLASK_APP=CodFuente.py

ENV FLASK_ENV=development

CMD flask run --host=0.0.0.0 

