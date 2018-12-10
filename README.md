# token-queue-system
Queue System Implementation Using Token with QR Code

## Requirements
* Python 3.5+

## Installation
1. Activate python virtual environment (if any)
2. Install requirements
```
pip install -r requirements.txt
```
3. Create database
```
python -c "from app import db; db.create_all()"
```
4. Run application with **sudo only**
```
sudo FLASK_ENV=development flask run
```