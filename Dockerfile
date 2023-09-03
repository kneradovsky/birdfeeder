FROM python:3.10-slim

WORKDIR /feeder

COPY requirements.txt requirements.txt
RUN python3 -m pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./

ENTRYPOINT [ "/bin/sh","/feeder/start.sh"]
