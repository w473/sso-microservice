FROM python:3.8
RUN apt-get update && apt-get install -y vim
COPY requirements.txt /var/www/requirements.txt
WORKDIR /var/www/app
RUN pip install -r /var/www/requirements.txt
CMD [ "flask", "run","--host=0.0.0.0","--port=5000" ]