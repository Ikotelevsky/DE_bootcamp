# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.12

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1


# Working directory
WORKDIR /app

# Install pip requirements
# COPY requirements.txt .
# COPY pipeline.py pipeline.py
RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2
COPY ingest_data.py ingest_data.py
ENTRYPOINT [ "python", "ingest_data.py" ]


