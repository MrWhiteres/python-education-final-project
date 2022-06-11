FROM python:3.10.5-buster
WORKDIR python-education-final-project
COPY . .
RUN pip install -r requirements.txt ;  chmod u+x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]