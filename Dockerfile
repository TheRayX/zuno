# ✅ Use a lightweight Python image
FROM python:3.10-slim

# ✅ Set the working directory
WORKDIR /app

# ✅ Copy everything into the container
COPY . .

# ✅ Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ✅ Expose the port that FastAPI will run on
EXPOSE 7860

# ✅ Run the FastAPI app (Hugging Face will hit port 7860)
CMD ["uvicorn", "api.zuno_bot1:app", "--host", "0.0.0.0", "--port", "7860"]
