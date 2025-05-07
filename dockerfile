FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10
COPY . /app
RUN pip install openai
ENV MODULE_NAME=main
ENV VARIABLE_NAME=app
