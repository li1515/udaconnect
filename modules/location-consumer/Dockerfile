FROM python:3.7-alpine

WORKDIR .

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev
COPY ./modules/location-consumer/requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000

COPY ./modules/location-consumer/ .
CMD ["python", "consumer.py"]
