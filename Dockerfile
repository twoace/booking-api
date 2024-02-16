FROM python:3.10
EXPOSE 8000
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY .. .
RUN chmod u+x ./entrypoint.sh
RUN chmod u+x ./wait-for-it.sh
ENTRYPOINT ["./entrypoint.sh"]