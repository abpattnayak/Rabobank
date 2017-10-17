FROM python:2.7
RUN apt-get update -qq && \
    apt-get install -qy htop iputils-ping lsof ltrace strace telnet vim && \
    rm -rf /var/lib/apt/lists/*
RUN wget -q https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2 && \
    tar -xjf phantomjs-2.1.1-linux-x86_64.tar.bz2 && \
    mv phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/bin && \
    rm -rf phantomjs-2.1.1-linux-x86_64.tar.bz2 phantomjs-2.1.1-linux-x86_64
ENV TERM xterm
ENV PYTHONPATH $PYTHONPATH:/app
ENV SCRAPY_SETTINGS_MODULE demo.settings
RUN mkdir -p /app
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
