# Use the official Python image with Streamlit support
FROM python:3.9-slim

# Set work directory
WORKDIR /app

# Install dependencies from requirements.txt
COPY requirements.txt .  
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files to the container
COPY . .

# Copy the store_document folder to the container (optional, adjust path if necessary)
COPY store_document /app/store_document

# Expose Streamlit port
EXPOSE 8501

# Run Streamlit app on container start
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
