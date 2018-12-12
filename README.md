# token-queue-system
Queue System Implementation Using Token with QR Code

## Requirements
* Python 3.5+

## Installation
**Note:** Always run flask command with `sudo -E` (preserved environment variable)

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
sudo -E flask init-db
```
6. Run application with **sudo only**
```
sudo -E flask run
```

## Create Manager
```
sudo -E flask create-manager
```