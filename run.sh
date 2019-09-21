#!/usr/bin/env bash
cmd="$1"
export ENV=online
export PORT=8089
export MYSQL_HOST=localhost
if [[ ${cmd} == "local" ]]; then
export MYSQL_PORT=3306
echo "start local"
python app.py
#gunicorn --workers=4 --threads=2 -b 0.0.0.0:${PORT} app:app
exit 0
elif [[ ${cmd} == "online" ]]; then
echo "start online"
export MYSQL_PORT=12580
gunicorn --workers=4 --threads=2 -b 0.0.0.0:${PORT} app:app -D;
else
echo "unknown command, use like `./run.sh local` or `./run.sh online` "
exit 0;
fi
