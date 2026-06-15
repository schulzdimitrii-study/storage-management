FROM python:3.13-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 3000

CMD ["python3", "app.py"]
