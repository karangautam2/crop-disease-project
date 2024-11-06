import os

def collect_logs(log_path):
    logs = []
    for root, dirs, files in os.walk(log_path):
        for file in files:
            with open(os.path.join(root, file), 'r') as f:
                logs.append(f.read())
    return logs

# Example usage
logs = collect_logs("/var/log/")
print(logs)
