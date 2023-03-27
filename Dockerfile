FROM ubuntu:20.04

EXPOSE 80

RUN apt update -y && \
    apt install software-properties-common -y && \
    add-apt-repository ppa:deadsnakes/ppa -y && \
    apt-get -y install python3-pip;

RUN apt install python3-numpy -y
RUN apt install python3-pandas -y

ADD install/requirements.txt  ./ 
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt -vvv

RUN mkdir /home/app
COPY src/ /home/app
ADD install/config.json /tmp/

CMD ["python3", "/home/app/send_message.py"]
