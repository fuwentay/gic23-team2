# Set base image (host OS)
FROM python:alpine3.8

# Set the working directory in the container
WORKDIR /app

# Copy the content of the project directory to the working directory
COPY . /app

RUN pip install --upgrade pip
# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Specify the Flask environment port
ENV PORT 9000

# By default, listen on port 5000
EXPOSE 9000

# Set the directive to specify the executable that will run when the container is initiated
ENTRYPOINT [ "python" ]

# Specify the command to run on container start
CMD [ "app.py" ]