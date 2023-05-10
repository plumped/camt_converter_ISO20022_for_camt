# syntax=docker/dockerfile:1
# Release 1.1.0

#Download Python from DockerHub and use it
FROM python:3.8-slim-buster

#Set the working directory in the Docker container
WORKDIR /app

#Copy the dependencies file to the working directory
COPY requirements.txt requirements.txt

#Install the dependencies
RUN pip3 install -r requirements.txt

#Copy the Flask app code to the working directory
COPY src/ .

#Run the container
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
