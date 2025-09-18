#!/bin/sh
while true; do
    #if ! /usr/bin/pgrep -f TestBot.py > /dev/null; then
        #echo "TestBot.py no está activo. Iniciando..."
        pkill -f TestBot.py
        python TestBot.py 2>&1 &
    #fi
    sleep 300
done &

python port.py
