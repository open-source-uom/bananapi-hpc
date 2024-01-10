#!/bin/bash

# Function to check and install packages
check_and_install() {
    local package_name="$1"
    dpkg -l "$package_name" &> /dev/null
    if [ $? -ne 0 ]; then
        echo "Installing $package_name..."
        sudo apt-get install -y "$package_name"
    else
        echo "$package_name is already installed."
    fi
}

# Function to download and install OpenMPI
install_openmpi() {
    local version="3.1.4"
    local big_version="3.1"
    local openmpi_url="https://download.open-mpi.org/release/open-mpi/v$big_version/openmpi-$version.tar.gz"
    
    # Download and extract OpenMPI
    echo "Downloading and installing OpenMPI $version..."
    wget "$openmpi_url"
    tar -xzvf "openmpi-$version.tar.gz"
    cd "openmpi-$version"
    
    # Configure, build, and install OpenMPI
    ./configure --prefix=/usr/local/openmpi-$version
    make
    sudo make install
    
    cd ..
    rm -rf "openmpi-$version" "openmpi-$version.tar.gz"
}

# List of required packages
packages=("libblas-dev" "other_package_name" "another_package_name")

# Update package information
sudo apt-get update

# Install required packages
for package in "${packages[@]}"; do
    check_and_install "$package"
done

# Install OpenMPI
install_openmpi

echo "All required packages and OpenMPI installed successfully."
# clone hpl repo and run it
git clone https://github.com/RIKEN-RCCS/hpl-ai.git
cd hpl-ai
make driver.out
OMP_NUM_THREADS=1 mpirun -n 4 ./driver.out 1200 60 2 -not -d -r
