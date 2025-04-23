import hashlib
from datetime import datetime


class Commit:
    def __init__(self, message):
        self.message = message
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Create a unique commit hash based on the message and date
        commit_str = f"{self.message}{self.date}"
        self.commit_hash = hashlib.sha256(commit_str.encode()).hexdigest()[:6]  # Shorten hash to 6 characters
