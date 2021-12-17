#! /bin/sh

echo "============================================================"
echo "Welcome to the setup. This will enable the local virtual env."
echo "And then it run the application."
echo "============================================================"

if [ -d ".env" ];
then
	echo "Enabling virtual env"
else
	echo "No Virtual env. Please run setup.sh first"
	exit 1
fi

#Activatimg virtual env
. .env/bin/activate
export ENV=development
python3 main.py
deactivate