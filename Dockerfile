FROM debian:buster
RUN apt update -y
RUN apt upgrade -y
RUN apt-get -y install apt-utils python3 python3-pip python3-dev git curl screen pkg-config libcairo2-dev libjpeg-dev libgif-dev nano
COPY app app
WORKDIR app
RUN pip3 install -r requirements.txt
EXPOSE 8082
CMD ./start_services.sh