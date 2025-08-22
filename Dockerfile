# Use a slim Python image as the base for a smaller final image size
FROM python:3.9-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt ./

# Install all Python dependencies from requirements.txt
# --no-cache-dir reduces image size by not storing build cache
RUN pip install --no-cache-dir -r requirements.txt

# Copy all your project files (app.py, random_forest_model.pkl, etc.) into the container
COPY . /app

# Expose the port that Streamlit runs on (default is 8501)
EXPOSE 8501

# Define the command to run your Streamlit application when the container starts
# --server.port 8501: ensures Streamlit listens on this port
# --server.enableCORS false: often needed for deployment environments
# --server.enableXsrfProtection false: often needed for deployment environments
CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.enableCORS", "false", "--server.enableXsrfProtection", "false"]