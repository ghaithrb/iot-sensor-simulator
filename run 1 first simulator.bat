@echo off
python main.py --host localhost --port 1883 --interval 1 --qos 0 --temp-center 22 --log-file data.json
pause