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
        export NVM_DIR="$HOME/.nvm"
        [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
        [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
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
    oldPythonVersion=$(python3 -V)
    oldPythonVersion=${oldPythonVersion//Python /}
    echo -n $'\n'"Actual python version is: "
    echo -n $'\e[1;32m'"$oldPythonVersion"$'\e[0m'
    read -p ", do you want to update it? (y/n): " pythonAnswer

    if [ "$pythonAnswer" != "${pythonAnswer#[Yy]}" ] ;then
        read -p "Which python version do you want to install?(ex: 3.11 or 3.12): " pythonVersion
        echo -n "Are you sure you want to install python version "
        echo -n $'\e[1;32m'"$pythonVersion"$'\e[0m'
        read -p "? (y/n): " pythonAnswer
        if [ "$pythonAnswer" != "${pythonAnswer#[Yy]}" ] ;then
            echo -n $'\n'"The python version to remove is: "$'\e[1;32m'"$oldPythonVersion"$'\e[0m'
            sudo rm -r /usr/lib/python3/dist-packages/*
            sudo apt remove python$oldPythonVersion -y
            sudo apt autoremove -y

            echo "Installing python version "$'\e[1;32m'"$pythonVersion"$'\e[0m'
            sudo apt install python$pythonVersion -y
            sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python$pythonVersion 1

            echo $'\n'"Showing old python versions"
            ls /usr/bin/python* | grep -v '\-config$'
            ls /usr/lib/python* | grep -v '\-config$'
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
clear
echo "------------------------------------------------------------------------------------"
echo "Updating and upgrading the system"
sudo apt update -y && sudo apt upgrade -y
sudo apt autoremove -y

# ---------------Install nodejs and npm using nvm---------------
echo $'\n'$'\e[1;32m'"---------------Install nodejs and npm using nvm---------------"$'\e[0m'
if ! command -v node &> /dev/null ;then
    echo $'\n'"Installing nvm, nodejs and npm"
    install_nvm_nodejs_npm
else
    echo $'\n'"Removing old nodejs and npm versions"
    sudo apt remove nodejs npm -y
    sudo apt purge nodejs npm -y
    install_nvm_nodejs_npm
fi

echo $'\n'$'\e[1;32m'"Installing dependencies for npm and nodejs"$'\e[0m'
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
echo $'\n'$'\e[1;32m'"---------------Installing npm libraries---------------"$'\e[0m'
echo $'\n'"Installing npm libraries"
npm install wait-port@1.1.0 --save-prod
npm install electron@8.1.0 electron-builder@24.9.1 --save-dev

# ---------------Installing python3---------------
echo $'\n'$'\e[1;32m'"---------------Installing python3---------------"$'\e[0m'
echo $'\n'"Verifying if python is installed"
# If python3 is not installed, then install it
if ! command -v python3 &> /dev/null ;then
    echo $'\n'"Installing python3"
    sudo apt install python3.11 -y
else
    python_installation
fi

# ---------------Installing pip---------------
echo $'\n'$'\e[1;32m'"---------------Installing pip---------------"$'\e[0m'
if ! command -v pip &> /dev/null ;then
    echo $'\n'"Installing pip"
    sudo apt install python3-pip -y
    print_pip_version
else
    echo $'\n'"Pip is already installed"
    print_pip_version
fi

# ---------------Installing python libraries---------------
echo $'\n'$'\e[1;32m'"---------------Installing python libraries---------------"$'\e[0m'
echo $'\n'"Installing python libraries"
pip install --upgrade setuptools
pip install -r requirements.txt

# ---------------Inits chmod for initsDevMode.sh---------------
echo $'\n'"Giving permissions to initsDevMode.sh"
chmod +x initsDevMode.sh

# ---------------Installing C libraries---------------
echo $'\n'$'\e[1;32m'"---------------Installing C libraries---------------"$'\e[0m'
sudo apt install gcc -y
# sudo apt-get install libcurl4-openssl-dev libminizip-dev -y

echo "------------------------------------------------------------------------------------"