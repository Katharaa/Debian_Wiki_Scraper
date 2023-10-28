FROM python:3.11

WORKDIR /app

COPY app.py requirements.txt urls.json /app/

ENV ENV=PROD

# Install required Python packages
RUN pip install -r requirements.txt

# Run the Python application(uses the default urls.json)
CMD ["python", "app.py"]