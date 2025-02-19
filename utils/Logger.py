class Logger:
    def __init__(self):
        self.log_file = "app.log"

    def add_to_log(self, level: str, message: str):
        with open(self.log_file, "a") as log:
            log.write(f"[{level.upper()}] {message}\n")