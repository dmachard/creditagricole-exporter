FROM python:3.12.7-alpine

LABEL name="Python Credit Agricole Exporter" \
      description="Python Credit Agricole Exporter" \
      url="https://github.com/dmachard/docker-creditagricole-exporter" \
      maintainer="d.machard@gmail.com"

WORKDIR /home/monitor
COPY . /home/monitor/

RUN apk update \
    && adduser -D monitor \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

USER monitor

ENTRYPOINT ["python", "-c", "import creditagricole_exporter as lib; lib.start_monitor();"]