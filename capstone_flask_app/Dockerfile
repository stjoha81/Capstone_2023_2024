# Use the official Python 3.8 slim image as the base image
FROM python:3.11

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

# Expose port 5000 for the Flask application
EXPOSE 5000

CMD python ./app.py
#CMD ["./app.py", "start"]
# CMD ["/path/to/my-cmd", "start"]  # Exec form with JSON array syntax