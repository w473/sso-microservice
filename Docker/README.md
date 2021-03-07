## source machine:

https://hub.docker.com/_/python

## build command:

docker build -t sso-py:latest .

## run:command:

docker-run.sh

## build - run commands from main dir

docker build -t docker.pkg.github.com/w473/sso-microservice/sso-ms:0.0.1 -f ./Docker/Dockerfile.build .

docker tag docker.pkg.github.com/w473/sso-microservice/sso-ms:0.0.1 docker.pkg.github.com/w473/sso-microservice/sso-ms:latest

docker push docker.pkg.github.com/w473/sso-microservice/sso-ms:0.0.1
