FROM python: 3.6.8

# ADD app.py .
WORKDIR /app
COPY . /app
EXPOSE 5000

RUN pip install -r requirements.txt

CMD ["python", "/main.py"]
