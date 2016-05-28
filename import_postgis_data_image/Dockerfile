FROM ubuntu

# Install Python.
RUN \
  apt-get update && \
  apt-get install -y python python-dev python-pip python-virtualenv && \
  rm -rf /var/lib/apt/lists/*

# Install Java.
RUN \
  apt-get update && \
  apt-get install -y openjdk-8-jdk && \
  rm -rf /var/lib/apt/lists/*

# Define working directory.
WORKDIR /data
COPY data /data
COPY osmosis_latest /data/osmosis_latest
# Define commonly used JAVA_HOME variable (for osimis)
ENV JAVA_HOME /usr/lib/jvm/java-7-openjdk-amd64

RUN apt-get update && apt-get install -y postgresql-client
COPY ./import_data.py /data/import_data.py
CMD [ "python", "import_data.py" ]
