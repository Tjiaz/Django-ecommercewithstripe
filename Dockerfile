FROM python:3 

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

# Copy the templates directory into the container
COPY templates /code/templates

# Copy the static directory into the container
COPY static /code/static

COPY . .

EXPOSE 8000

CMD ["python3","manage.py","runserver"]