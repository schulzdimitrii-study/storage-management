FROM python:3.13-alpine

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install flask requests

COPY . /app

EXPOSE 5000

CMD ["python3", "app.py"]
