FROM python:3.10
EXPOSE 8000
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY .. .
ENV GUNICORN_CMD_ARGS="-w 4 --bind 0.0.0.0:8000"
CMD ["gunicorn", "bookingapp:create_app()"]