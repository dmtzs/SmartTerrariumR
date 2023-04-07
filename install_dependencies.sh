#!/bin/bash

# Ask user for desired Python version
read -p "Which version of Python do you want to install? (e.g. 3.10 or 3.11): " python_version

# Check if the desired Python version is already installed
if [[ $(python${python_version} --version 2>&1) == *"Python ${python_version}"* ]]; then
  echo "Python ${python_version} is already installed."
else
  # Find the latest available version of the desired series
  latest_version=$(curl -s "https://www.python.org/ftp/python/" | grep -Eo "href=\"3.${python_version}\.[0-9]+/" | sed "s/href=\"3.${python_version}\.//" | sed "s/\/.*//g" | sort -n | tail -n 1)

  if [ -z "$latest_version" ]; then
    echo "No versions of Python 3.${python_version} are available."
    exit 1
  else
    # Download and install the latest available version of the desired series
    echo "Downloading Python 3.${python_version}.${latest_version} source code..."
    wget https://www.python.org/ftp/python/3.${python_version}/Python-3.${python_version}.${latest_version}.tar.xz

    echo "Extracting Python 3.${python_version}.${latest_version} source code..."
    tar -xf Python-3.${python_version}.${latest_version}.tar.xz

    cd Python-3.${python_version}.${latest_version}

    echo "Configuring Python 3.${python_version}.${latest_version} build..."
    ./configure --enable-optimizations

    echo "Building and installing Python 3.${python_version}.${latest_version}..."
    sudo make altinstall

    # Verify Python version
    echo "Verifying Python version..."
    if [[ $(python${python_version} --version 2>&1) == *"Python ${python_version}"* ]]; then
      echo "Python ${python_version} installed successfully."
    else
      echo "Failed to install Python ${python_version}."
      exit 1
    fi

    # Clean up the installation files
    echo "Cleaning up installation files..."
    cd ..
    rm Python-3.${python_version}.${latest_version}.tar.xz
    rm -r Python-3.${python_version}.${latest_version}
  fi
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt
if [ $? -eq 0 ]; then
    echo "Python dependencies installed successfully."
else
    echo "Failed to install Python dependencies."
fi

# Install curl
echo "Installing curl..."
sudo apt install curl
if [ $? -eq 0 ]; then
    echo "curl installed successfully."
else
    echo "Failed to install curl."
fi

# Install Node.js
echo "Installing Node.js..."
curl -sL https://deb.nodesource.com/setup_14.x | sudo bash -
cat /etc/apt/sources.list.d/nodesource.list
sudo apt update
sudo apt install -y nodejs
if [ $? -eq 0 ]; then
    echo "Node.js installed successfully."
else
    echo "Failed to install Node.js."
fi

# Install npm packages
echo "Installing npm packages..."
npm install wait-port --save-prod
npm install electron electron-builder --save-dev
if [ $? -eq 0 ]; then
    echo "npm packages installed successfully."
else
    echo "Failed to install npm packages."
fi

echo "All commands have been executed."