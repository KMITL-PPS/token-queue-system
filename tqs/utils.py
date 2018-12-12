import os

from tqs.functions.config import load_config
from tqs.functions.key import load_key


# load setting
queue_interval = os.environ.get('QUEUE_INTERVAL', 5000)

# load config/key
load_config()
load_key()
