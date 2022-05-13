#!/usr/bin/bash
cd /home/dmtzs/Documentos/SmartTerrariumR/TelegramScripts
/usr/bin/python3 "telegram_alerts.py" "--rebootRasp"
/usr/bin/python3 commandsTelegram.py &

cd /home/dmtzs/Documentos/SmartTerrariumR
DISPLAY=:0 npm start

# pkill -xf "/usr/bin/python3 commandsTelegram.py"