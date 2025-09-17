#!/bin/sh
while true; do
    if ! pgrep -f TestBot.py > /dev/null; then
        echo "TestBot.py no está activo. Iniciando..."
        python TestBot.py 2>&1 &
    fi
    sleep 5
done &

python port.py
