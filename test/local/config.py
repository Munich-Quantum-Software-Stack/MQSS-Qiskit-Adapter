"""Testing Configuration"""

import os

TOKEN = None
try:
    TOKEN = os.environ["MQP_TOKEN"]
except KeyError:
    print("set MQP_TOKEN to your MQP token in the environment.")

# NOTE: change to current backend names
BACKENDS = ["QExa20"]
URL = "https://portal.quantum.lrz.de:4000"
