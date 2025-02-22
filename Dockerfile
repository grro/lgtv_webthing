FROM python:3.11

ENV port 8080
ENV ip_address 0.0.0.0
ENV dir /app/store


RUN cd /etc
RUN mkdir app
WORKDIR /etc/app
ADD *.py /etc/app/
ADD requirements.txt /etc/app/.
RUN pip install -r requirements.txt

CMD python /etc/app/tv_webthing.py $port $ip_address $dir


