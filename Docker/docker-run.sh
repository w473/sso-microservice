#/bin/bash
docker run -d -p 5000:5000 --env-file="$(pwd)/../.env" \
--env FLASK_APP="/var/www/app/flaskr" \
--mount type=bind,source="$(pwd)/..",target=/var/www/app \
sso-py:latest