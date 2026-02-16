from datetime import datetime, timezone, timedelta

def is_market_open():
    now = datetime.now(timezone(timedelta(hours=7)))
    if now.weekday() >= 5:
        return False
    if now.hour < 9:
        return False
    if 12 <= now.hour < 13:
        return False
    if now.hour >= 16:
        return False
    return True
