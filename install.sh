#!/bin/bash
if if ! [ -x "$(command -v crew)" ];  then curl -Ls git.io/vddgY | bash; fi
crew install python27 eudev
pip install python-uinput
cd ~
curl -Ls https://raw.githubusercontent.com/kishorv06/ChromePad/master/GamePad.py > GamePad.py
cp GamePad.py /usr/local/bin/GamePad.py
printf "#!/bin/bash\n sudo -s\n modprob uinput\n python GamePad.py\n" > /usr/local/bin/ChromePad
chmod a+x /usr/local/bin/ChromePad
echo "Installed ChromePad."
echo "To run enter 'chromepad' in shell"
