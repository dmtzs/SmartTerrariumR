#!/usr/bin/bash

# ---------------Functions---------------
install_nvm_nodejs_npm() {
    echo $'\n'"Installing nvm (node version manager) to install nodejs and npm"
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh
    read -p "Do you want to continue with the nodejs and npm installation? (y/n): " answer

    # If the answer is yes, then continue with the installation
    if [ "$answer" != "${answer#[Yy]}" ] ;then
        echo $'\n'"Installing nvm"
        curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
        source ~/.bashrc
        # validates if nvm was installed correctly and if not finish the script
        if ! command -v nvm &> /dev/null
        then
            echo $'\n'"nvm could not be installed, finishing the script"
            exit
        fi
        nvm list-remote
        read -p "Which nodejs version do you want to install from the list?: " nodejsVersion

        echo $'\n'"Installing nodejs version $nodejsVersion"
        nvm install $nodejsVersion
        nodeVersion=$(node -v)
        npmVersion=$(npm -v)

        echo -n $'\n'"Nodejs version: "
        echo $'\e[1;32m'"$nodeVersion"$'\e[0m'

        echo -n "Npm version: "
        echo $'\e[1;32m'"$npmVersion"$'\e[0m'
    else
        echo $'\n'"Nodejs and npm installation canceled"
    fi
}

python_installation() {
    echo $'\n'"Verifying python version"
    pythonVersion=$(python3 -V)
    pythonVersion=${pythonVersion//Python /}
    echo -n $'\n'"Actual python version is: "
    echo -n $'\e[1;32m'"$pythonVersion"$'\e[0m'
    read -p ", do you want to update it? (y/n): " pythonAnswer

    if [ "$pythonAnswer" != "${pythonAnswer#[Yy]}" ] ;then
        read -p "Which python version do you want to install?(ex: 3.11 or 3.12): " pythonVersion
        echo -n "Are you sure you want to install python version "
        echo -n $'\e[1;32m'"$pythonVersion"$'\e[0m'
        read -p "? (y/n): " pythonAnswer
        if [ "$pythonAnswer" != "${pythonAnswer#[Yy]}" ] ;then
            echo "Installing python version "$'\e[1;32m'"$pythonVersion"$'\e[0m'
            sudo apt install python$pythonVersion -y
            sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python$pythonVersion 1

            echo $'\n'"Showing old python versions"
            ls /usr/bin/python* | grep -v '\-config$'

            pythonVersions=$(ls -1 /usr/bin/python3.* | grep -Eo 'python3\.[0-9]+' | grep -vE '(\-config$|python3\.11$)' | sort -u)
            echo -n $'\n'"The python versions to remove are: "
            echo $'\e[1;32m'"$pythonVersions"$'\e[0m'
            pythonVersions=($pythonVersions)  # python versions from string to array
            for pythonVersion in "${pythonVersions[@]}"; do
                echo "Removing python version $pythonVersion"
                sudo rm -r /usr/lib/$pythonVersion/
                sudo rm -r /usr/bin/$pythonVersion/
            done
        else
            echo "Python update canceled"
        fi
    else
        echo "Python update canceled"
    fi
}

print_pip_version() {
    pipVersion=$(pip -V)
    echo -n $'\n'"Pip version installed: "
    echo $'\e[1;32m'"$pipVersion"$'\e[0m'
}

# ---------------Updating and upgrading the system---------------
echo "------------------------------------------------------------------------------------"
echo "Updating and upgrading the system"
sudo apt update -y && sudo apt upgrade -y

# ---------------Install nodejs and npm using nvm---------------
if ! command -v node &> /dev/null ;then
    echo $'\n'"Installing nvm, nodejs and npm"
    install_nvm_nodejs_npm
else
    echo $'\n'"Removing old nodejs and npm versions"
    sudo apt remove nodejs npm -y
    sudo apt purge nodejs npm -y
    install_nvm_nodejs_npm

echo $'\n'"Installing dependencies for npm and nodejs"
# Using step 3 of the next tutorial https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-ubuntu-22-04#option-3-installing-node-using-the-node-version-manager
sudo apt-get install libnss3 -y
sudo apt-get install libatk1.0-0 -y
sudo apt-get install libatk-bridge2.0-0 -y
sudo apt-get install libcups2 -y
sudo apt-get install libgdk-pixbuf2.0-0 -y
sudo apt-get install libgtk-3-0 -y
sudo apt-get install libgbm1 -y
sudo apt-get install libasound2 -y

# ---------------Installing npm libraries---------------
echo $'\n'"Installing npm libraries"
npm install wait-port@1.1.0 --save-prod
npm install electron@8.1.0 electron-builder@24.9.1 --save-dev

# ---------------Installing python3---------------
echo $'\n'"Verifying if python is installed"
# If python3 is not installed, then install it
if ! command -v python3 &> /dev/null ;then
    echo $'\n'"Installing python3"
    sudo apt install python3.11 -y
else
    python_installation
fi

# ---------------Installing pip---------------
if ! command -v pip &> /dev/null ;then
    echo $'\n'"Installing pip"
    sudo apt install python3-pip -y
    print_pip_version
else
    echo $'\n'"Pip is already installed"
    print_pip_version
fi

# ---------------Installing python libraries---------------
echo $'\n'"Installing python libraries"
pip install -r requirements.txt

# ---------------Inits chmod for initsDevMode.sh---------------
echo $'\n'"Giving permissions to initsDevMode.sh"
chmod +x initsDevMode.sh
echo "------------------------------------------------------------------------------------"
