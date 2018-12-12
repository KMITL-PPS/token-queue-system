# token-queue-system
Queue System Implementation Using Token with QR Code

## Requirements
* Python 3.5+

## Installation
**Note:** Always run with sudo permission

1. Activate python virtual environment (if any)
2. Get into project's root directory
```
cd token-queue-system
```
3. Install requirements
```
pip install -r requirements.txt
```
4. Set Flask environment variable
```
export FLASK_APP=tqs/app
export FLASK_ENV=development
```
5. Init database
```
sudo flask init-db
```
6. Run application with **sudo only**
```
sudo flask run
```

## Create Manager
```
sudo flask create-manager
```