import logging
import os
from datetime import datetime

os.makedirs("logs", exist_ok=True)
log_file = f"logs/sme_{datetime.now().strftime('%Y%m%d')}.log"

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

def get_logger(name):
    return logging.getLogger(name)