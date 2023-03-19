FROM ubuntu:20.04

EXPOSE 80

RUN apt update -y && \
    apt install software-properties-common -y && \
    add-apt-repository ppa:deadsnakes/ppa -y && \
    apt-get -y install python3-pip;

ADD install/requirements.txt  ./ 

RUN pip3 install -r requirements.txt 

RUN mkdir /home/app
COPY src/ /home/app
ADD install/config.json /tmp/

CMD ["python3", "/home/app/send_message.py"]