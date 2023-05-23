FROM python:3.9

WORKDIR /app

ENV DAGSTER_HOME=/app/.dagster_home
RUN ln -s /app/.aws /root

COPY requirements.txt /app
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
CMD ["flask", "--app", "main", "run", "--host=0.0.0.0"]
