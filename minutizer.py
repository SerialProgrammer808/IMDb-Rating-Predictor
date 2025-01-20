import re

def minutizer(time_str):
    # Use regex to extract hours and minutes (both optional)
    match = re.match(r"(?:(\d+)\s*h)?\s*(?:(\d+)\s*m)?", str(time_str))
    
    # Extract hours and minutes, default to 0 if not present
    hours = int(match.group(1)) if match.group(1) else 0
    minutes = int(match.group(2)) if match.group(2) else 0
    
    # Convert to total minutes
    total_minutes = hours * 60 + minutes
    return total_minutes

