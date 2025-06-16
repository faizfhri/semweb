FROM openjdk:11-jdk-slim

# Install curl & unzip
RUN apt-get update && apt-get install -y curl unzip

# Download & extract GraphDB
RUN curl -L -o graphdb.zip https://download.ontotext.com/graphdb/graphdb-11.0.1-dist.zip && \
    unzip graphdb.zip && \
    mv graphdb-11.0.1 graphdb && \
    rm graphdb.zip

# Copy config & data
COPY config.ttl /config.ttl
COPY data.ttl /data.ttl

# Run GraphDB and import data
CMD bash -c "\
    ./graphdb/bin/graphdb & \
    sleep 15 && \
    curl -X POST http://localhost:7200/rest/repositories \
         -H 'Content-Type: multipart/form-data' \
         -F config=@/config.ttl && \
    curl -X POST http://localhost:7200/repositories/myrepo/statements \
         -H 'Content-Type: text/turtle' --data-binary @/rectoverso.ttl && \
    tail -f /dev/null"
