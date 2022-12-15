FROM python:3.8-slim

# For psycopg to install
RUN apt-get update \
    && apt-get -y install libpq-dev gcc 
 
RUN mkdir /myapp
WORKDIR /myapp

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disc (equivalent to python -B option)
# PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr (equivalent to python -u option)

RUN pip install --upgrade pip
COPY requirements.txt /myapp/

   
RUN pip install -r /myapp/requirements.txt

COPY . /myapp/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]