FROM python:3.10-slim

RUN apt update -y && apt install awscli -y && apt install libgomp1

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8000

# Run the FastAPI application using uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]