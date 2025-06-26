# utils.py

import json
from config import PROCESSED_LOG

def load_log():
    try:
        with open(PROCESSED_LOG, 'r') as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()

def save_log(log_set):
    with open(PROCESSED_LOG, 'w') as f:
        json.dump(list(log_set), f)
