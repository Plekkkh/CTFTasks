FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    curl \
    cron \
    supervisor \
    netcat-traditional \
    && rm -rf \
    /var/lib/apt/lists/*

RUN pip3 install flask requests gunicorn -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN chsh -s /bin/bash www-data

WORKDIR /app

COPY external_app.py internal_app.py /app/
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY templates/ /app/templates/
COPY static/ /app/static/

RUN chown -R root:root /app && \
    chmod -R 755 /app

RUN mkdir -p /var/www/html/reports /backup && \
    chown -R www-data:www-data /var/www/html/reports /backup && \
    chmod -R 755 /var/www/html/reports /backup

RUN echo "* * * * * root cd /var/www/html/reports && tar -cf /backup/reports.tar * >/dev/null 2>&1\n" >> /etc/crontab


EXPOSE 8080
CMD ["sh", "-c", "echo \"$CTF_FLAG\" > /root/flag.txt && chmod 400 /root/flag.txt && unset CTF_FLAG && exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf"]