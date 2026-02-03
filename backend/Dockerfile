FROM python:3.10

WORKDIR /app


COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt --default-timeout=100

# Copy logic (though docker-compose volumes will override this in dev)
COPY . .

# Expose the port
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
