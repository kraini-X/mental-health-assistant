# Use Python 3.10 (or whatever you want)
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose the port Gradio uses
EXPOSE 7860

# Default command
CMD ["python", "ui.py"]
