# Use a base image with Python
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the full app
COPY . .

# Expose port
EXPOSE 7860

# Run the FastAPI app using uvicorn
CMD ["uvicorn", "zuno_bot1:app", "--host", "0.0.0.0", "--port", "7860"]
