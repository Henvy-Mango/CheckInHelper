FROM python:3-alpine

ENV CRON_SIGNIN='0 6 * * *' \
    TZ=Asia/Shanghai

WORKDIR /tmp
COPY requirements.txt ./
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories  && \
    adduser app -D             && \
    apk add --no-cache tzdata  && \
    pip install --no-cache-dir -r requirements.txt  && \
    pip install --no-cache-dir crontab              && \
    rm -rf /tmp/*

WORKDIR /app
COPY docker.py ./
COPY checkinhelper ./checkinhelper

USER app
CMD [ "python3", "./docker.py" ]
