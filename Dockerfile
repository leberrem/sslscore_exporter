FROM python:3

RUN pip install requests && \
    pip install pytz && \
    pip install python-dateutil && \
    pip install prometheus_client

ADD exporter.py /
COPY ssllabs /ssllabs
COPY httpobscli /httpobscli

EXPOSE 9299/tcp

CMD [ "python", "-u", "./exporter.py" ]