#!/usr/bin/bash
cd /home/dmtzs/Documentos
/usr/bin/python3 "telegram1.py" "--rebootRasp"
/usr/bin/python3 commandsTelegram.py &

cd /home/dmtzs/Documentos/SmartTerrariumR
DISPLAY=:0 npm start

# pkill -xf "python3 commandsTelegram.py"