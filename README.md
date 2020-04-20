# REASPOSTWEB

install firefox on server ubuntu/debian
https://unix.stackexchange.com/questions/395316/install-firefox-quantum-in-debian-9-stretch

install geckodriver
cd /bin/
sudo wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
sudo tar -xvf geckodriver-v0.26.0-linux64.tar.gz
sudo rm -f geckodriver-v0.26.0-linux64.tar.gz
sudo chmod +x geckodriver

install google chrome on ubuntu/debian
https://www.linuxbabe.com/ubuntu/install-google-chrome-ubuntu-18-04-lts

install chromedriver
cd /bin
wget https://chromedriver.storage.googleapis.com/81.0.4044.69/chromedriver_linux64.zip
unzip chromedriver_linux64.zip;
chmod +x chromedriver;
rm -f chromedriver_linux64.zip

start python django service
cd /project/path
python3 -W "ignore" manage.py runserver 0.0.0.0:8080 --insecure >> /dev/null 2>&1 &
