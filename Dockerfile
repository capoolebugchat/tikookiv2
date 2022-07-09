FROM python:3.9-slim
COPY . .
run pip install --upgrade pip
run pip install -r requirements.txt
CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker  --threads 8 server:app