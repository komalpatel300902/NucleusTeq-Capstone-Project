# Use the official Python image from the Docker Hub
FROM python:3.7.4

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt .

# Install dependencies using pip
RUN pip install -r requirements.txt

# Copy the entire current directory into the container at /app
COPY . .

# Expose port 80 to allow external access
EXPOSE 8000

# Command to run the FastAPI application using Uvicorn server
CMD ["uvicorn", "main:app", "--reload"]
