FROM scrapinghub/scrapinghub-stack-scrapy:1.3
RUN wget -q https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2 && \
    tar -xjf phantomjs-2.1.1-linux-x86_64.tar.bz2 && \
    mv phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/bin && \
    rm -rf phantomjs-2.1.1-linux-x86_64.tar.bz2 phantomjs-2.1.1-linux-x86_64
RUN pip install selenium
RUN mkdir -p /root/selenium_wd_tests
ADD sel_wd_new_user.py /root/selenium_wd_tests
ADD xvfb.init /etc/init.d/xvfb
RUN chmod +x /etc/init.d/xvfb
RUN update-rc.d xvfb defaults
CMD (service xvfb start; export DISPLAY=:10; python /root/selenium_wd_tests/sel_wd_new_user.py)
ENV TERM xterm
ENV SCRAPY_SETTINGS_MODULE Rabobank.settings
RUN mkdir -p /app
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
RUN python setup.py install
