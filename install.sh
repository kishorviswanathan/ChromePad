#!/bin/bash

INSTALLDIR=/usr/local/bin

printf "Installing / Updating ChromePad\n"

# Install crew if required
if ! [ -x "$(command -v crew)" ];  then 
  printf "Installing ChromeBrew\n"
  curl -Ls git.io/vddgY | bash
fi

# Install python
printf "Installing Python & Udev Library \n"
yes | crew install python3 eudev
printf "Installing Python Module \n"
sudo python3 -m pip install python-uinput

# Install ChromePad
printf "Copying ChromePad files to %s \n" $INSTALLDIR

# Remove old files
sudo rm $INSTALLDIR/chromepad $INSTALLDIR/GamePad.py 2>/dev/null

# Download GamePad.py
if ! [ -f "GamePad.py" ]; then
  curl -Ls https://raw.githubusercontent.com/kishorv06/ChromePad/master/GamePad.py > GamePad.py
fi
chmod a+x GamePad.py
mv GamePad.py $INSTALLDIR

# Generate wrapper script
sudo tee $INSTALLDIR/chromepad << EOF >> /dev/null
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
python3 $INSTALLDIR/GamePad.py
EOF
sudo chmod a+x $INSTALLDIR/chromepad

echo "Successfully installed ChromePad."
