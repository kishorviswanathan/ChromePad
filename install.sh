#!/bin/bash
curl -Ls git.io/vddgY | bash
crew install python27 eudev
pip install python-uinput
cd ~
curl -Ls https://raw.githubusercontent.com/kishorv06/ChromePad/master/GamePad.py > GamePad.py
cp GamePad.py /usr/lib/bin/GamePad.py
printf "#!/bin/bash\n sudo -s\n modprob uinput\n python GamePad.py\n" > /usr/lib/bin/ChromePad
chmod a+x /usr/lib/bin/ChromePad
