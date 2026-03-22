FROM python:3.12-slim

RUN apt-get update && apt-get install -y python3 python3-pip curl cron supervisor netcat-traditional && rm -rf /var/lib/apt/lists/*
RUN pip3 install flask requests

RUN chsh -s /bin/bash www-data

WORKDIR /app
COPY external_app.py internal_app.py /app/
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

COPY templates/ /app/templates/
COPY static/ /app/static/

RUN mkdir -p /var/www/html/reports /backup
RUN chown -R www-data:www-data /var/www/html/reports /backup

RUN echo "* * * * * root cd /var/www/html/reports && tar -cf /backup/reports.tar * >/dev/null 2>&1\n" >> /etc/crontab


EXPOSE 80
CMD ["sh", "-c", "echo \"$CTF_FLAG\" > /root/flag.txt && chmod 400 /root/flag.txt && /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf"]