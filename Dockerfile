
FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    curl \
    apt-utils \
    lsb-release \
    gnupg \
    wget \
    libssl-dev \
    liblzo2-dev \
    libpcap0.8-dev \
    iputils-ping

# Download and install Surfshark
RUN curl -f https://downloads.surfshark.com/linux/debian-install.sh --output /surfshark-install.sh
RUN sh surfshark-install.sh

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY setup_vpn.py .

# Copy the auth file into the container
COPY auth.txt .

# Update pip
RUN pip install --upgrade pip

# Copy the rest of the application code into the container
COPY . .

# Define the command to run your script when the container starts
CMD ["python","setup_vpn.py"]



# # Copy the script to the Docker image
# COPY setup_vpn.sh /usr/local/bin/setup_vpn.sh

# # Make the script executable
# RUN chmod +x /usr/local/bin/setup_vpn.sh