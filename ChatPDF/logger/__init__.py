import logging
import os
from datetime import datetime

from from_root import from_root

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y')}.log"

log_dir = "logs"

logs_path = os.path.join(from_root(), log_dir, LOG_FILE)

os.makedirs(log_dir, exist_ok=True)


logging.basicConfig(
    filename=logs_path,
    format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
