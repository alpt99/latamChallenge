# syntax=docker/dockerfile:1.2
FROM python:3.9
# put you docker configuration here
WORKDIR /code

COPY requirements.txt /code/requirements.txt
COPY requirements-dev.txt /code/requirements-dev.txt
COPY requirements-test.txt /code/requirements-test.txt

RUN python -m pip install --upgrade pip setuptools

RUN pip install --no-cache-dir --upgrade -r /code/requirements-dev.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements-test.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
# RUN pip install -r /code/requirements.txt

COPY ./ /code/

# CMD ["make", "model-test"]
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]