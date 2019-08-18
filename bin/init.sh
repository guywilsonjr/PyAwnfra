#!/usr/bin/env bash
export REPO_NAME='PyAwnfra'
# To install run chmod +x env/{REPO_NAME}bin/init.sh && yes | ENV/{REPO_NAME}/init.sh
rm ~/environment/README.md

sudo yum -y update
sudo yum -y upgrade
cd /usr/src
sudo wget https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tgz
sudo tar xzf Python-3.7.3.tgz
sudo rm Python-3.7.3.tgz
cd Python-3.7.3
sudo ./configure --enable-optimizations
sudo make altinstall
cd ~/environment/
sudo rm -rf /usr/src/Python-3.7.3
sudo alternatives --set python /usr/bin/python3.7
python3 -m venv env
cd env

sudo update-alternatives --config python

# Configure git
git clone https://github.com/guywilsonjr/${REPO_NAME}
cd ${REPO_NAME}
git config credential.helper 'cache --timeout=999999'
# git config --global credential.helper '!aws codecommit credential-helper $@'
git config --global credential.UseHttpPath true
git pull


curl -O https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py --user
rm get-pip.py
npm install -g aws-cdk
source ../bin/activate
pip install --upgrade pip
pip install -r requirements.txt

deactivate
echo 'source /home/ec2-user/environment/PyAwnfraEnv/PyAwnfra/bin/reinit.sh' >> ~/.zshrc