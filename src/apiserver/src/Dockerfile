FROM python:3.13

RUN apt-get update && apt-get install -y python3-pip

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENTRYPOINT ["python3"]

CMD ["-m", "openapi_server"]
