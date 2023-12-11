# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install cron
RUN apt update
RUN apt -y install cron

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Add the cron job
RUN crontab -l | { cat; echo "*/5 * * * * python shrinkarr.main"; } | crontab -

# Replace 'entrypoint' in docker-compose or 'command' in Kubernetes with 'cron' to manage cronjob in container
CMD ["python", "shrinkarr.main"]
