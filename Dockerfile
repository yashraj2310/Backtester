# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /code

# Copy the dependencies file to the working directory first
# This allows Docker to cache the installed packages
COPY ./requirements.txt /code/requirements.txt

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# --- KEY CHANGE IS HERE ---
# Copy the rest of the application's source code from your local machine to the container
COPY . /code/

# Command to run when the container starts
# It ensures the Prisma client is generated before starting the server
CMD ["sh", "-c", "prisma generate && uvicorn app.main:app --host 0.0.0.0 --port 8000"]