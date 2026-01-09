import datetime
import logging


class Logger:
    def __init__(self, file_level=logging.INFO, console_level=logging.INFO):
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        fh = logging.FileHandler(f"log_{current_datetime}.txt")
        fh.setLevel(file_level)
        ch = logging.StreamHandler()
        ch.setLevel(console_level)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def log(self, message, level=logging.INFO):
        self.logger.log(
            level,
            f"{message}",
        )
