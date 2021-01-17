FROM python:3.8
RUN apt-get update && apt-get install -y vim
COPY requirements.txt /var/www/requirements.txt
WORKDIR /var/www/app
RUN python3 -m ensurepip --upgrade
RUN pip3 install -r /var/www/requirements.txt
CMD [ "flask", "run","--host=0.0.0.0","--port=5000" ]