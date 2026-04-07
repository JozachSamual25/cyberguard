failed_attempts = {}

def detect_attack(username, password):
    patterns = ["'", "--", " OR ", "1=1"]

    # SQL Injection Detection
    for p in patterns:
        if p in username or p in password:
            return ("SQL Injection", "HIGH")

    # Brute Force Detection
    failed_attempts[username] = failed_attempts.get(username, 0) + 1

    if failed_attempts[username] > 5:
        return ("Brute Force", "CRITICAL")

    return (None, None)


def reset_attempts(username):
    if username in failed_attempts:
        failed_attempts[username] = 0