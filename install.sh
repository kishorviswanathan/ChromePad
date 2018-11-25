#!/bin/bash
printf "Installing / Updating ChromePad\n\n"
if ! [ -x "$(command -v crew)" ];  then 
  printf "Installing ChromeBrew\n\n"
  curl -Ls git.io/vddgY | bash
fi
printf "Installing Python & Udev Library \n\n"
crew install python27 eudev
printf "Installing Python Module \n\n"
pip install python-uinput
printf "Copying ChromePad files to /usr/local/bin/ \n\n"
cd ~
sudo rm /usr/local/bin/chromepad /usr/local/bin/GamePad.py 2>/dev/null
curl -Ls https://raw.githubusercontent.com/kishorv06/ChromePad/master/GamePad.py > GamePad.py
cp GamePad.py /usr/local/bin/GamePad.py
sudo cat <<EOT >> /usr/local/bin/chromepad 
#!/bin/bash
printf "[    ]  Checking if user is root"
if ! [[ \$EUID = 0 ]]; then
  printf "\rPlease run as root. ie sudo chromepad \n"
  exit
fi
printf "\r[ OK ]  Checking if user is root\n"
printf "[    ]  Loading uinput module"
modprobe uinput
printf "\r[ OK ]  Loading uinput module\n"
printf "[ OK ]  Starting ChromePad Server\n"
clear
python /usr/local/bin/GamePad.py
EOT
sudo chmod a+x /usr/local/bin/chromepad
echo "Successfully installed ChromePad."
