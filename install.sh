#!/bin/bash
echo "Installing / Updating ChromePad"
if ! [ -x "$(command -v crew)" ];  then curl -Ls git.io/vddgY | bash; fi
crew install python27 eudev
pip install python-uinput
cd ~
sudo rm /usr/local/bin/chromepad /usr/local/bin/GamePad.py 2>/dev/null
curl -Ls https://raw.githubusercontent.com/kishorv06/ChromePad/master/GamePad.py > GamePad.py
cp GamePad.py /usr/local/bin/GamePad.py
sudo cat <<EOT >> /usr/local/bin/chromepad 
#!/bin/bash
if ! [[ \$EUID = 0 ]]; then
  echo "Please run as root. ie sudo chromepad"
  exit
fi
modprobe uinput
python GamePad.py
EOT
sudo chmod a+x /usr/local/bin/chromepad
echo "Successfully installed ChromePad."
