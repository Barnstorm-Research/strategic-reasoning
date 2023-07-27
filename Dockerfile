FROM python:latest

RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get -y install vim 

COPY requirements.txt /home/requirements.txt

COPY src /home/src

WORKDIR /home

RUN pip3 install -r requirements.txt

WORKDIR /home/src

CMD ["bash"]