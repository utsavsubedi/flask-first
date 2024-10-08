FROM python:3.12.2

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip \
    && pip install -r requirements.txt


COPY  . /app/

EXPOSE 5000

CMD ["flask", "run", "--host", "0.0.0.0"]