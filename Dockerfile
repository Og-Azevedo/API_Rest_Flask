# from alpine:latest
#
# # RUN apk add --no-cache python3-dev\&& pip3 install --upgrade pip
#
# WORKDIR /app
# COPY requirements.txt requirements.txt
# COPY . /app
#
# # RUN pip3 --no-cache-dir install -r requirements.txt
# RUN pip3 install -r requirements.txt
# EXPOSE 5000
#
# ENTRYPOINT ["python3"]
# CMD ["app.py"]


FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
COPY banco.db banco.db
RUN pip3 install -r requirements.txt
# EXPOSE 5000

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]