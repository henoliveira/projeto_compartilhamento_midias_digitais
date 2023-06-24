FROM python:3.11-slim

RUN mkdir /usr/src/app/
COPY . /usr/src/app/
WORKDIR /usr/src/app/
EXPOSE 8000

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
CMD ["uvicorn", "main:app", "--reload", "--workers=4", "--host=0.0.0.0", "--port=1337"]
