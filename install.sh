#!/bin/bash
echo "Installing / Updating ChromePad"
if ! [ -x "$(command -v crew)" ];  then curl -Ls git.io/vddgY | bash; fi
crew install python27 eudev
pip install python-uinput
cd ~
curl -Ls https://raw.githubusercontent.com/kishorv06/ChromePad/master/GamePad.py > GamePad.py
sudo cp GamePad.py /usr/local/bin/GamePad.py
sudo rm /usr/local/bin/chromepad /usr/local/bin/GamePad.py 2>/dev/null
sudo cat <<EOT >> /usr/local/bin/chromepad 
#!/bin/bash
sudo -s
modprob uinput
python GamePad.py
EOT
sudo chmod a+x /usr/local/bin/chromepad
echo "Installed ChromePad."
echo "To run enter chromepad in shell"
