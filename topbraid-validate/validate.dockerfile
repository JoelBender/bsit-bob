FROM azul/zulu-openjdk-debian:11-jre-latest

RUN echo 'APT::Install-Suggests "0";' >> /etc/apt/apt.conf.d/00-docker
RUN echo 'APT::Install-Recommends "0";' >> /etc/apt/apt.conf.d/00-docker

RUN apt update -qy

RUN echo 'tzdata tzdata/Areas select America' | debconf-set-selections
RUN echo 'tzdata tzdata/Zones/America select New_York' | debconf-set-selections
RUN apt install -y tzdata
RUN apt install -y zip unzip git default-jre

RUN apt install -y python3-dev python3-pip python3-venv

WORKDIR /app

COPY requirements.txt .
RUN python3 -m venv venv \
    && . venv/bin/activate \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

COPY shacl-1.4.2/ shacl-1.4.2/
COPY validate.py .
COPY 223standard.ttl .

CMD ["venv/bin/python", "validate.py"]
