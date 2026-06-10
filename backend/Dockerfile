FROM python:3.13-alpine

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "[IP_ADDRESS]", "--port", "8000", "--reload"]
