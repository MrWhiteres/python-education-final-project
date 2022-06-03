FROM python:3.10
EXPOSE 8000
WORKDIR flask_project
COPY requirements.txt .
RUN apt-get update; apt-get install -y postgresql-client; rm -rf /var/cache/apt
RUN pip install -r requirements.txt
COPY flask_project/ .
RUN chmod u+x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]