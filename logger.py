from datetime import datetime

def log_signal(text):
    with open("signals_log.txt", "a", encoding="utf-8") as f:
        f.write(f"\n{datetime.now()}\n")
        f.write(text)
        f.write("\n----------------------\n")