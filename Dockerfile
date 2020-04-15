FROM amancevice/pandas:latest

EXPOSE 80

RUN pip install --upgrade pip \
     && pip install gunicorn falcon

COPY ./app /app
WORKDIR /app

CMD ["gunicorn", "-b", "0.0.0.0:80", "main:app"]

