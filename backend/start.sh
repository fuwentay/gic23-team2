if [[ "$(docker ps -aq -f name=gic-flask)" ]]; then
    # Check if the container is running
    if [[ "$(docker inspect -f '{{.State.Running}}' gic-flask)" == "true" ]]; then
        # Stop the running container
        echo "Stopping the running container gic-flask..."
        docker stop gic-flask
    fi

    # Delete the container
    echo "Deleting the container gic-flask..."
    docker rm gic-flask
fi

docker build -t lgwayne/flask-container:1.0.0 .
docker run --name gic-flask -p 5000:5000 lgwayne/flask-container:1.0.0