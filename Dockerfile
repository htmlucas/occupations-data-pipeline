FROM python:3.14-alpine
WORKDIR /app
COPY requirements.txt .
run pip install -r requirements.txt
COPY . .
#CMD ["python","src/main.py"]