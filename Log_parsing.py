import re

class LogSystem:
    def __init__(self, capacity=5):
        self.capacity = capacity
        self.recent_logs = []
        self.user_logs = {}
        self.level_count = {}

    def parse_log(self, line):
        match = re.match(r"\[(.*?)\] (\w+) (\w+): (.+)", line)
        if not match:
            print("Invalid log format:", line)
            return None
        timestamp, level, user_id, message = match.groups()
        return {
            "timestamp": timestamp,
            "level": level,
            "user_id": user_id,
            "message": message
        }

    def add_log(self, line):
        log = self.parse_log(line)
        if log is None:
            return
        self.recent_logs.append(log)
        if len(self.recent_logs) > self.capacity:
            self.recent_logs.pop(0)
        user = log["user_id"]
        if user not in self.user_logs:
            self.user_logs[user] = []
        self.user_logs[user].append(log)
        level = log["level"]
        if level not in self.level_count:
            self.level_count[level] = 0
        self.level_count[level] += 1

    def get_user_logs(self, user_id):
        return self.user_logs.get(user_id, [])

    def count_levels(self):
        return self.level_count

    def filter_logs(self, keyword):
        result = []
        for log in self.recent_logs:
            if keyword.lower() in log["message"].lower():
                result.append(log)
        return result

    def get_recent_logs(self):
        return self.recent_logs

logs = [
    "[2025-06-16T10:00:00] INFO user1: Started process",
    "[2025-06-16T10:00:01] ERROR user1: Failed to connect",
    "[2025-06-16T10:00:02] INFO user2: Login successful",
    "[2025-06-16T10:00:03] WARN user3: Low memory",
    "[2025-06-16T10:00:04] ERROR user2: Timeout occurred",
    "[2025-06-16T10:00:05] INFO user1: Retrying connection"
]

logger = LogSystem(capacity=5)
for log in logs:
    logger.add_log(log)

print("User1 logs:", logger.get_user_logs("user1"))
print("Level count:", logger.count_levels())
print("Filter 'connect':", logger.filter_logs("connect"))
print("Recent logs:", logger.get_recent_logs())
