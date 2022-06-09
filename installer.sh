sudo apt update
sudo apt install -y git mosquitto python3 python3-pip

cd /opt

if [ -d "Pi-StopWatch" ]
then
        echo "project - directory allready exists"
else
        sudo git clone https://github.com/Manfe07/Pi-StopWatch.git
fi

cd Pi-StopWatch

cp config.json.example config.json

pip install -r flask_backend/requirements.txt
pip install -r stopwatch_core/requirements.txt

sudo cp stopwatch_flask.service /etc/systemd/system/
sudo cp stopwatch_core.service /etc/systemd/system/

sudo systemctl enable stopwatch_core
sudo systemctl enable stopwatch_flask

sudo systemctl start stopwatch_core
sudo systemctl start stopwatch_flask
