FROM python:3.12

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV PORT=8000

EXPOSE $PORT

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
